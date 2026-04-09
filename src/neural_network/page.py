import json
import pandas as pd
import streamlit as st

from src.neural_network.predict import predict_admission
from src.logging_config import get_logger

logger = get_logger(__name__)

METRICS_PATH = "models/neural_network_metrics.json"
DATA_PATH = "data/Admission.csv"


def load_metrics():
    logger.info("Loading neural network metrics from %s", METRICS_PATH)
    try:
        with open(METRICS_PATH, "r", encoding="utf-8") as f:
            metrics = json.load(f)
            logger.info("Metrics loaded successfully")
            return metrics
    except FileNotFoundError:
        logger.warning("Metrics file not found")
        return None


def load_data():
    logger.info("Loading dataset from %s", DATA_PATH)
    df = pd.read_csv(DATA_PATH)
    logger.info("Dataset loaded with shape=%s", df.shape)
    return df


def render_neural_network_page():
    logger.info("Rendering neural network page")

    st.header("Admission Classification using Neural Network")
    st.write("Classify applicants as likely above or below the notebook-defined admission threshold using an MLPClassifier model.")

    tabs = st.tabs(["Overview", "EDA", "Model", "Predict"])

    metrics = load_metrics()
    df = load_data()

    # ---------------- OVERVIEW ----------------
    with tabs[0]:
        st.markdown(
            """
            This module classifies graduate applicants based on academic profile features.

            **Dataset:** `Admission.csv`  
            **Target:** Binary admission label derived from `Admit_Chance`  
            **Task type:** Classification  
            **Model used in deployed app:** Neural Network (`MLPClassifier`)  
            **Positive class definition:** `Admit_Chance >= 0.80`
            """
        )

        st.markdown("### Business Context")
        st.write(
            """
            This model simulates an admission screening workflow by classifying applicants
            based on academic and profile-based features.
            """
        )

        st.markdown("### Input Features")
        feature_df = pd.DataFrame(
            {
                "Feature": [
                    "GRE Score", "TOEFL Score", "University Rating",
                    "SOP", "LOR", "CGPA", "Research"
                ],
                "Description": [
                    "Graduate Record Examination score",
                    "TOEFL English proficiency score",
                    "Institution rating",
                    "Statement of purpose strength",
                    "Recommendation strength",
                    "Undergraduate performance",
                    "Research experience"
                ],
            }
        )
        st.dataframe(feature_df, width="stretch")

    # ---------------- EDA ----------------
    with tabs[1]:
        st.markdown("### Original Admit Chance Distribution")
        st.bar_chart(df["Admit_Chance"].value_counts().sort_index())

        st.markdown("### Numeric Feature Summary")
        numeric_cols = [
            "GRE_Score", "TOEFL_Score", "University_Rating",
            "SOP", "LOR", "CGPA", "Research", "Admit_Chance",
        ]
        existing_numeric_cols = [col for col in numeric_cols if col in df.columns]
        st.dataframe(df[existing_numeric_cols].describe().T, width="stretch")

        st.markdown("### Key Observations")
        st.write(
            """
            - GRE and CGPA are strong indicators
            - Research improves outcomes
            - SOP and LOR add supporting signal
            """
        )

    # ---------------- MODEL ----------------
    with tabs[2]:
        st.markdown("### Model Performance")

        if metrics is None:
            st.warning("Metrics file not found. Run training script.")
        else:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Accuracy", f"{metrics['Accuracy']:.4f}")
            c2.metric("Precision", f"{metrics['Precision']:.4f}")
            c3.metric("Recall", f"{metrics['Recall']:.4f}")
            c4.metric("F1 Score", f"{metrics['F1']:.4f}")

            st.markdown("### Confusion Matrix")
            cm_df = pd.DataFrame(
                metrics["Confusion_Matrix"],
                index=["Actual 0", "Actual 1"],
                columns=["Predicted 0", "Predicted 1"],
            )
            st.dataframe(cm_df, width="stretch")

    # ---------------- PREDICT ----------------
    with tabs[3]:
        st.subheader("Interactive Prediction")

        with st.form("neural_network_prediction_form"):
            col1, col2 = st.columns(2)

            with col1:
                gre = st.number_input("GRE Score", 0, 340, 320)
                toefl = st.number_input("TOEFL Score", 0, 120, 105)
                university_rating = st.selectbox("University Rating", [1, 2, 3, 4, 5])
                sop = st.selectbox("SOP", [1.0,2.0,3.0,4.0,5.0])

            with col2:
                lor = st.selectbox("LOR", [1.0,2.0,3.0,4.0,5.0])
                cgpa = st.number_input("CGPA", 0.0, 10.0, 8.5)
                research_text = st.selectbox("Research", ["No", "Yes"])

            submitted = st.form_submit_button("Predict")

        if submitted:
            logger.info("Neural network prediction requested")

            try:
                input_data = {
                    "GRE_Score": gre,
                    "TOEFL_Score": toefl,
                    "University_Rating": university_rating,
                    "SOP": sop,
                    "LOR": lor,
                    "CGPA": cgpa,
                    "Research": 1 if research_text == "Yes" else 0,
                }

                result = predict_admission(input_data)
                logger.info("Prediction result: %s", result)

                predicted_class = result["predicted_class"]
                probability = result["probability"]

                if predicted_class == 1:
                    st.success("Prediction: High Admission Likelihood")
                else:
                    st.warning("Prediction: Low Admission Likelihood")

                if probability is not None:
                    st.info(f"Probability: {probability:.2%}")

                st.markdown("### Input Summary")
                st.dataframe(pd.DataFrame([input_data]), width="stretch")

            except Exception:
                logger.exception("Error during neural network prediction")
                st.error("An error occurred during prediction.")