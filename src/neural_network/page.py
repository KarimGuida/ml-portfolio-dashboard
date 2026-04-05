import json
import streamlit as st
import pandas as pd

from src.neural_network.predict import predict_admission
from src.neural_network.eda import load_data, summary, numeric_summary
from src.neural_network.visuals import plot_target_distribution, plot_scatter

METRICS_PATH = "models/neural_network_metrics.json"


def load_metrics():
    try:
        with open(METRICS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def render_neural_network_page():
    st.header("Admission Prediction using Neural Network")
    st.write("Predict admission probability using an MLPRegressor model.")

    tabs = st.tabs(["Overview", "EDA", "Model", "Predict"])

    df = load_data()

    with tabs[0]:
        st.subheader("Project Overview")
        st.markdown(
            """
            This project predicts graduate admission chance using academic profile features.

            **Dataset:** `Admission.csv`  
            **Target:** `Admit_Chance`  
            **Task type:** Regression  
            **Model used in deployed app:** Neural Network (`MLPRegressor`)
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

        st.markdown("### Admit Chance Distribution")
        st.pyplot(plot_target_distribution(df))

        st.markdown("### Summary Statistics")
        st.dataframe(numeric_summary(df), width="stretch")

        plot_cols = [col for col in ["GRE_Score", "CGPA"] if col in df.columns]
        if len(plot_cols) == 2:
            col1, col2 = st.columns(2)
            with col1:
                st.pyplot(plot_scatter(df, plot_cols[0]))
            with col2:
                st.pyplot(plot_scatter(df, plot_cols[1]))

    with tabs[2]:
        st.subheader("Model Performance")
        metrics = load_metrics()

        if metrics is None:
            st.warning("Metrics file not found. Run the training script again.")
        else:
            c1, c2, c3 = st.columns(3)
            c1.metric("MAE", f"{metrics['MAE']:.4f}")
            c2.metric("RMSE", f"{metrics['RMSE']:.4f}")
            c3.metric("R²", f"{metrics['R2']:.4f}")

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
        st.write("Enter applicant academic details to estimate admission chance.")
        st.caption("Use realistic academic values based on the dataset scale.")

        with st.form("admission_form"):
            left_col, right_col = st.columns(2)

            with left_col:
                gre_score = st.number_input(
                    "GRE Score",
                    min_value=260,
                    max_value=340,
                    value=320,
                    step=1,
                    help="Typical GRE score range in the dataset."
                )

                toefl_score = st.number_input(
                    "TOEFL Score",
                    min_value=0,
                    max_value=120,
                    value=105,
                    step=1,
                    help="TOEFL score."
                )

                university_rating = st.selectbox(
                    "University Rating",
                    [1, 2, 3, 4, 5],
                    index=2,
                    help="Institution rating from 1 to 5."
                )

                sop = st.selectbox(
                    "Statement of Purpose (SOP)",
                    [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
                    index=6,
                    help="SOP strength rating."
                )

            with right_col:
                lor = st.selectbox(
                    "Letter of Recommendation (LOR)",
                    [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
                    index=6,
                    help="Recommendation strength rating."
                )

                cgpa = st.number_input(
                    "CGPA",
                    min_value=0.0,
                    max_value=10.0,
                    value=8.5,
                    step=0.1,
                    help="CGPA on a 10-point scale."
                )

                research_label = st.selectbox(
                    "Research Experience",
                    ["Yes", "No"],
                    help="Whether the applicant has research experience."
                )

            submitted = st.form_submit_button("Predict Admission Chance")

        if submitted:
            inputs = {
                "GRE_Score": float(gre_score),
                "TOEFL_Score": float(toefl_score),
                "University_Rating": float(university_rating),
                "SOP": float(sop),
                "LOR": float(lor),
                "CGPA": float(cgpa),
                "Research": 1.0 if research_label == "Yes" else 0.0,
            }

            try:
                prediction = predict_admission(inputs)

                st.success(f"Predicted Admission Chance: {prediction:.2%}")

                if prediction >= 0.8:
                    st.write("This profile indicates a strong admission chance.")
                elif prediction >= 0.6:
                    st.write("This profile indicates a moderate admission chance.")
                else:
                    st.write("This profile indicates a lower admission chance.")

                st.markdown("### Input Summary")
                

                st.dataframe(pd.DataFrame([inputs]), width="stretch")

            except Exception as e:
                st.error(f"Error: {e}")