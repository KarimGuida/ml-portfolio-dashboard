import json
import streamlit as st
import pandas as pd

from src.real_estate.predict import predict_price
from src.real_estate.eda import load_data, summary, numeric_summary
from src.real_estate.visuals import plot_price_distribution

METRICS_PATH = "models/real_estate_metrics.json"


def load_metrics():
    try:
        with open(METRICS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def render_real_estate_page():
    st.header("Real Estate Price Prediction")
    st.write("Regression project for predicting house sale prices.")

    tabs = st.tabs(["Overview", "EDA", "Model", "Predict"])

    df = load_data()

    with tabs[0]:
        st.subheader("Project Overview")
        st.markdown(
            """
            This project predicts house prices using structured property features.

            **Dataset:** `final.csv`  
            **Target:** `price`  
            **Task type:** Regression  
            **Model used in deployed app:** Random Forest Regressor inside a preprocessing pipeline
            """
        )

        stats = summary(df)
        c1, c2, c3 = st.columns(3)
        c1.metric("Rows", stats["rows"])
        c2.metric("Columns", stats["cols"])
        c3.metric("Missing Values", stats["missing"])

        st.subheader("Preview")
        st.dataframe(df.head(10), width="stretch")

    with tabs[1]:
        st.subheader("Exploratory Data Analysis")

        st.markdown("### Price Distribution")
        st.pyplot(plot_price_distribution(df))

        st.markdown("### Numeric Summary")
        st.dataframe(numeric_summary(df), width="stretch")

    with tabs[2]:
        st.subheader("Model Performance")
        metrics = load_metrics()

        if metrics is None:
            st.warning("Metrics file not found. Run the training script again.")
        else:
            c1, c2, c3 = st.columns(3)
            c1.metric("MAE", f"{metrics['MAE']:.2f}")
            c2.metric("RMSE", f"{metrics['RMSE']:.2f}")
            c3.metric("R²", f"{metrics['R2']:.4f}")

            st.markdown("### Training Information")
            info_df = pd.DataFrame(
                {
                    "Metric": ["Train Rows", "Test Rows", "Number of Features"],
                    "Value": [
                        metrics["train_shape"][0],
                        metrics["test_shape"][0],
                        len(metrics["features"]),
                    ],
                }
            )
            st.dataframe(info_df, width="stretch")

    with tabs[3]:
        st.subheader("Interactive Prediction")
        st.write("Enter property details to estimate the predicted sale price.")
        st.caption("Inputs follow the ranges observed in the dataset.")

        with st.form("real_estate_form"):
            left_col, right_col = st.columns(2)

            with left_col:
                year_sold = st.number_input(
                    "Year Sold",
                    min_value=1993,
                    max_value=2016,
                    value=2010,
                    step=1,
                    help="Year when the property was sold."
                )

                property_tax = st.number_input(
                    "Property Tax",
                    min_value=88,
                    max_value=4508,
                    value=450,
                    step=1,
                    help="Property tax amount in dataset units."
                )

                insurance = st.number_input(
                    "Insurance",
                    min_value=30,
                    max_value=1374,
                    value=140,
                    step=1,
                    help="Insurance amount in dataset units."
                )

                beds = st.number_input(
                    "Bedrooms",
                    min_value=1,
                    max_value=5,
                    value=3,
                    step=1
                )

                baths = st.number_input(
                    "Bathrooms",
                    min_value=1,
                    max_value=6,
                    value=2,
                    step=1
                )

                sqft = st.number_input(
                    "Living Area (sq ft)",
                    min_value=500,
                    max_value=7842,
                    value=2200,
                    step=10
                )

                lot_size = st.number_input(
                    "Lot Size",
                    min_value=0,
                    max_value=436471,
                    value=8000,
                    step=100,
                    help="Lot size in dataset units."
                )

            with right_col:
                year_built = st.number_input(
                    "Year Built",
                    min_value=1880,
                    max_value=2014,
                    value=1995,
                    step=1
                )

                basement_label = st.selectbox(
                    "Basement",
                    ["Yes", "No"]
                )

                popular_label = st.selectbox(
                    "Popular Area",
                    ["Yes", "No"]
                )

                recession_label = st.selectbox(
                    "Recession Period",
                    ["Yes", "No"]
                )

                property_age = st.number_input(
                    "Property Age",
                    min_value=0,
                    max_value=114,
                    value=15,
                    step=1
                )

                condo_label = st.selectbox(
                    "Property Type",
                    ["House", "Condo"]
                )

            submitted = st.form_submit_button("Predict Price")

        if submitted:
            input_data = {
                "year_sold": int(year_sold),
                "property_tax": int(property_tax),
                "insurance": int(insurance),
                "beds": int(beds),
                "baths": int(baths),
                "sqft": int(sqft),
                "year_built": int(year_built),
                "lot_size": int(lot_size),
                "basement": 1 if basement_label == "Yes" else 0,
                "popular": 1 if popular_label == "Yes" else 0,
                "recession": 1 if recession_label == "Yes" else 0,
                "property_age": int(property_age),
                "property_type_Condo": 1 if condo_label == "Condo" else 0,
            }

            try:
                predicted_price = predict_price(input_data)

                st.success(f"Predicted Price: ${predicted_price:,.0f}")
                st.write("This estimate is based on the trained regression model and the property features you entered.")

                st.markdown("### Input Summary")
                input_summary = pd.DataFrame([{
                    "Year Sold": year_sold,
                    "Property Tax": property_tax,
                    "Insurance": insurance,
                    "Bedrooms": beds,
                    "Bathrooms": baths,
                    "Living Area (sq ft)": sqft,
                    "Year Built": year_built,
                    "Lot Size": lot_size,
                    "Basement": basement_label,
                    "Popular Area": popular_label,
                    "Recession Period": recession_label,
                    "Property Age": property_age,
                    "Property Type": condo_label,
                }])

                st.dataframe(input_summary, width="stretch")

            except Exception as e:
                st.error(f"Error: {e}")