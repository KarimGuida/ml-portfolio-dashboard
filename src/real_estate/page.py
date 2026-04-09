import json
import streamlit as st
import pandas as pd

from src.real_estate.predict import predict_price
from src.real_estate.eda import load_data, summary, numeric_summary
from src.real_estate.visuals import plot_price_distribution
from src.logging_config import get_logger

logger = get_logger(__name__)

METRICS_PATH = "models/real_estate_metrics.json"


def load_metrics():
    logger.info("Loading real estate metrics from %s", METRICS_PATH)
    try:
        with open(METRICS_PATH, "r", encoding="utf-8") as f:
            metrics = json.load(f)
            logger.info("Metrics loaded successfully")
            return metrics
    except FileNotFoundError:
        logger.warning("Metrics file not found")
        return None


def render_real_estate_page():
    logger.info("Rendering real estate page")

    st.header("Real Estate Price Prediction")
    st.write("Regression project for predicting house sale prices.")

    tabs = st.tabs(["Overview", "EDA", "Model", "Predict"])

    logger.info("Loading dataset")
    df = load_data()
    logger.info("Dataset loaded with shape=%s", df.shape)

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
                year_sold = st.number_input("Year Sold", 1993, 2016, 2010)
                property_tax = st.number_input("Property Tax", 88, 4508, 450)
                insurance = st.number_input("Insurance", 30, 1374, 140)
                beds = st.number_input("Bedrooms", 1, 5, 3)
                baths = st.number_input("Bathrooms", 1, 6, 2)
                sqft = st.number_input("Living Area (sq ft)", 500, 7842, 2200)
                lot_size = st.number_input("Lot Size", 0, 436471, 8000)

            with right_col:
                year_built = st.number_input("Year Built", 1880, 2014, 1995)
                basement_label = st.selectbox("Basement", ["Yes", "No"])
                popular_label = st.selectbox("Popular Area", ["Yes", "No"])
                recession_label = st.selectbox("Recession Period", ["Yes", "No"])
                property_age = st.number_input("Property Age", 0, 114, 15)
                condo_label = st.selectbox("Property Type", ["House", "Condo"])

            submitted = st.form_submit_button("Predict Price")

        if submitted:
            logger.info("Real estate prediction requested")

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

            logger.info("Input data prepared for prediction")

            try:
                predicted_price = predict_price(input_data)
                logger.info("Prediction successful: price=%s", predicted_price)

                st.success(f"Predicted Price: ${predicted_price:,.0f}")

                st.markdown("### Input Summary")
                st.dataframe(pd.DataFrame([input_data]), width="stretch")

            except Exception:
                logger.exception("Error during real estate prediction")
                st.error("An error occurred during prediction.")