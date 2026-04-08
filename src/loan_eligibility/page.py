import json
import pandas as pd
import streamlit as st

from src.loan_eligibility.predict import predict_loan_eligibility
from src.loan_eligibility.eda import (
    load_raw_data,
    get_dataset_summary,
    get_missing_values,
    get_numeric_summary,
    get_target_distribution,
    get_approval_by_category,
    get_clean_feature_frame,
)
from src.loan_eligibility.visuals import (
    plot_target_distribution,
    plot_loan_amount_distribution,
    plot_applicant_income_distribution,
    plot_approval_by_category,
    plot_correlation_heatmap,
)

METRICS_PATH = "models/loan_eligibility_metrics.json"


def load_metrics():
    try:
        with open(METRICS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None


def render_loan_eligibility_page():
    st.header("Loan Eligibility Prediction")
    st.write("Classification project for predicting whether a loan application will be approved.")

    tabs = st.tabs(["Overview", "EDA", "Model", "Predict"])

    df = load_raw_data()
    clean_df = get_clean_feature_frame(df)

    with tabs[0]:
        st.subheader("Project Overview")
        st.markdown(
            """
            This project predicts whether a loan application is likely to be approved.

            **Dataset:** `credit.csv`  
            **Target:** `Loan_Approved`  
            **Task type:** Classification  
            **Model used in deployed app:** Random Forest inside a preprocessing pipeline
            """
        )

        summary = get_dataset_summary(df)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Rows", summary["rows"])
        c2.metric("Columns", summary["columns"])
        c3.metric("Missing Values", summary["missing_values"])
        c4.metric("Duplicate Rows", summary["duplicate_rows"])

        st.subheader("Preview")
        st.dataframe(df.head(10), width="stretch")

    with tabs[1]:
        st.subheader("Exploratory Data Analysis")

        st.markdown("### Missing Values")
        st.dataframe(get_missing_values(df), width="stretch")

        st.markdown("### Numeric Summary")
        st.dataframe(get_numeric_summary(df), width="stretch")

        target_df = get_target_distribution(df)
        st.markdown("### Loan Approval Distribution")
        st.pyplot(plot_target_distribution(target_df))

        col1, col2 = st.columns(2)
        with col1:
            st.pyplot(plot_applicant_income_distribution(df))
        with col2:
            st.pyplot(plot_loan_amount_distribution(df))

        st.markdown("### Approval by Credit History")
        credit_df = get_approval_by_category(df, "Credit_History")
        st.pyplot(plot_approval_by_category(credit_df, "Credit_History"))

        st.markdown("### Approval by Property Area")
        property_df = get_approval_by_category(df, "Property_Area")
        st.pyplot(plot_approval_by_category(property_df, "Property_Area"))

        st.markdown("### Correlation Heatmap")
        st.pyplot(plot_correlation_heatmap(clean_df))

    with tabs[2]:
        st.subheader("Model Performance")
        metrics = load_metrics()

        if metrics is None:
            st.warning("Metrics file not found. Run the training script again.")
        else:
            c1, c2, c3 = st.columns(3)
            c1.metric("Accuracy", f"{metrics['accuracy']:.2%}")
            c2.metric("Train Rows", metrics["train_shape"][0])
            c3.metric("Test Rows", metrics["test_shape"][0])

            st.markdown("### Confusion Matrix")
            cm = metrics["confusion_matrix"]

            cm_df = pd.DataFrame(
                {
                    "Predicted 0": [cm[0][0], cm[1][0]],
                    "Predicted 1": [cm[0][1], cm[1][1]],
                },
                index=["Actual 0", "Actual 1"],
            )
            st.dataframe(cm_df, width="stretch")

            st.markdown("### Classification Report")
            report_df = pd.DataFrame(metrics["classification_report"]).transpose()
            st.dataframe(report_df, width="stretch")

    with tabs[3]:
        st.subheader("Interactive Prediction")
        st.write("Enter applicant details to evaluate loan approval likelihood.")

        with st.form("loan_prediction_form"):

            col1, col2 = st.columns(2)

            with col1:
                gender = st.selectbox("Gender", ["Male", "Female"], index=0)
                married = st.selectbox("Married", ["Yes", "No"], index=0)
                dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"], index=0)
                education = st.selectbox("Education Level", ["Graduate", "Not Graduate"], index=0)
                self_employed = st.selectbox("Self-Employed", ["Yes", "No"], index=0)
                property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"], index=0)

            with col2:
                applicant_income = st.number_input(
                    "Applicant Income (dataset units)",
                    min_value=0.0,
                    value=5000.0,
                    step=100.0
                )
                coapplicant_income = st.number_input(
                    "Coapplicant Income (dataset units)",
                    min_value=0.0,
                    value=0.0,
                    step=100.0
                )
                loan_amount = st.number_input(
                    "Loan Amount (likely in thousands)",
                    min_value=0.0,
                    value=120.0,
                    step=1.0
                )
                loan_term = st.selectbox(
                    "Loan Term (months)",
                    [12, 36, 60, 84, 120, 180, 240, 300, 360],
                    index=8
                )
                credit_history_text = st.selectbox(
                    "Credit History",
                    ["Good (1)", "Poor (0)"],
                    index=0
                )

            submitted = st.form_submit_button("Predict")

        if submitted:
            input_data = {
                "Gender": gender,
                "Married": married,
                "Dependents": dependents,
                "Education": education,
                "Self_Employed": self_employed,
                "ApplicantIncome": applicant_income,
                "CoapplicantIncome": coapplicant_income,
                "LoanAmount": loan_amount,
                "Loan_Amount_Term": float(loan_term),
                "Credit_History": 1.0 if credit_history_text == "Good (1)" else 0.0,
                "Property_Area": property_area,
            }

            try:
                result = predict_loan_eligibility(input_data)

                if result["prediction"] == "Y":
                    st.success("✅ Loan is likely to be APPROVED")
                    st.write("The applicant profile matches patterns associated with approved loans.")
                else:
                    st.error("❌ Loan is likely to be REJECTED")
                    st.write("The applicant profile does not match typical approval patterns.")

                if result["confidence"] is not None:
                    st.info(f"Confidence: {result['confidence']:.2%}")

                st.markdown("### Input Summary")
                input_summary = pd.DataFrame([{
                    "Gender": gender,
                    "Married": married,
                    "Dependents": dependents,
                    "Education": education,
                    "Self_Employed": self_employed,
                    "ApplicantIncome": applicant_income,
                    "CoapplicantIncome": coapplicant_income,
                    "LoanAmount": loan_amount,
                    "Loan_Amount_Term": loan_term,
                    "Credit_History": 1.0 if credit_history_text == "Good (1)" else 0.0,
                    "Property_Area": property_area,
                }])
                st.dataframe(input_summary, width="stretch")

            except Exception as e:
                st.error(f"Error: {e}")