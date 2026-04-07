import json
import pandas as pd
import streamlit as st

from src.neural_network.predict import predict_admission

METRICS_PATH = "models/neural_network_metrics.json"
DATA_PATH = "data/Admission.csv"


def load_metrics():
    with open(METRICS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_data():
    return pd.read_csv(DATA_PATH)


def render_neural_network_page():
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
            based on academic and profile-based features. It is intended to identify profiles
            that meet a predefined admission threshold for analysis purposes.
            """
        )

        st.markdown("### Input Features")
        feature_df = pd.DataFrame(
            {
                "Feature": [
                    "GRE Score",
                    "TOEFL Score",
                    "University Rating",
                    "Statement of Purpose (SOP)",
                    "Letter of Recommendation (LOR)",
                    "CGPA",
                    "Research Experience",
                ],
                "Description": [
                    "Graduate Record Examination score",
                    "TOEFL English proficiency score",
                    "Institution rating",
                    "Strength of statement of purpose",
                    "Strength of recommendation letters",
                    "Undergraduate academic performance",
                    "Whether the applicant has research experience",
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
            "GRE_Score",
            "TOEFL_Score",
            "University_Rating",
            "SOP",
            "LOR",
            "CGPA",
            "Research",
            "Admit_Chance",
        ]
        existing_numeric_cols = [col for col in numeric_cols if col in df.columns]
        st.dataframe(df[existing_numeric_cols].describe().T, width="stretch")

        st.markdown("### Key Observations")
        st.write(
            """
            - GRE Score and CGPA are strong academic indicators associated with higher admission outcomes.
            - Research experience tends to improve applicant competitiveness.
            - SOP and LOR provide supporting signal alongside quantitative performance measures.
            - The original target variable is continuous, but the deployed application uses a classification threshold for decision modeling.
            """
        )

    # ---------------- MODEL ----------------
    with tabs[2]:
        st.markdown("### Model Performance")

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

        st.markdown("### Model Overview")
        st.write(
            """
            The deployed model is a neural network classifier trained to identify applicants
            likely to meet the admission threshold defined in the notebook logic.

            The pipeline includes:
            - missing value handling
            - numerical feature scaling
            - neural network classification using `MLPClassifier`
            """
        )

        st.markdown("### Metric Interpretation")
        st.write(
            """
            - **Accuracy** measures overall classification correctness.
            - **Precision** reflects how reliable positive predictions are.
            - **Recall** indicates how effectively the model captures strong applicant profiles.
            - **F1 Score** balances precision and recall in a single summary metric.
            """
        )

        if "target_definition" in metrics:
            st.caption(f"Target definition: {metrics['target_definition']}")

    # ---------------- PREDICT ----------------
    with tabs[3]:
        st.subheader("Interactive Prediction")
        st.write("Enter applicant academic details to classify whether the profile is likely to meet the admission threshold.")

        with st.form("neural_network_prediction_form"):
            col1, col2 = st.columns(2)

            with col1:
                gre = st.number_input("GRE Score", min_value=0, max_value=340, value=320, step=1)
                toefl = st.number_input("TOEFL Score", min_value=0, max_value=120, value=105, step=1)
                university_rating = st.selectbox("University Rating", [1, 2, 3, 4, 5], index=2)
                sop = st.selectbox("Statement of Purpose (SOP)", [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0], index=6)

            with col2:
                lor = st.selectbox("Letter of Recommendation (LOR)", [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0], index=6)
                cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, value=8.5, step=0.1)
                research_text = st.selectbox("Research Experience", ["No", "Yes"], index=1)

            submitted = st.form_submit_button("Predict Admission Class")

        if submitted:
            research = 1 if research_text == "Yes" else 0

            input_data = {
                "GRE_Score": gre,
                "TOEFL_Score": toefl,
                "University_Rating": university_rating,
                "SOP": sop,
                "LOR": lor,
                "CGPA": cgpa,
                "Research": research,
            }

            result = predict_admission(input_data)

            predicted_class = result["predicted_class"]
            probability = result["probability"]

            st.markdown("### Prediction Result")

            if predicted_class == 1:
                st.success("Prediction: High Admission Likelihood")
            else:
                st.warning("Prediction: Low Admission Likelihood")

            if probability is not None:
                st.info(f"Estimated probability of positive class: {probability:.2%}")

            st.markdown("### Interpretation")
            if predicted_class == 1:
                st.write("This applicant profile is classified above the admission threshold used in the notebook.")
            else:
                st.write("This applicant profile is classified below the admission threshold used in the notebook.")

            st.markdown("### Input Summary")
            input_summary = pd.DataFrame([input_data])
            st.dataframe(input_summary, width="stretch")