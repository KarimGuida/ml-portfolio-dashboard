FEATURE_COLUMNS = [
    "Gender",
    "Married",
    "Dependents",
    "Education",
    "Self_Employed",
    "ApplicantIncome",
    "CoapplicantIncome",
    "LoanAmount",
    "Loan_Amount_Term",
    "Credit_History",
    "Property_Area",
]

TARGET_COLUMN = "Loan_Approved"
DROP_COLUMNS = ["Loan_ID"]

CATEGORICAL_COLUMNS = [
    "Gender",
    "Married",
    "Dependents",
    "Education",
    "Self_Employed",
    "Property_Area",
]

NUMERICAL_COLUMNS = [
    "ApplicantIncome",
    "CoapplicantIncome",
    "LoanAmount",
    "Loan_Amount_Term",
    "Credit_History",
]

ALLOWED_VALUES = {
    "Gender": ["Male", "Female"],
    "Married": ["Yes", "No"],
    "Dependents": ["0", "1", "2", "3+"],
    "Education": ["Graduate", "Not Graduate"],
    "Self_Employed": ["Yes", "No"],
    "Property_Area": ["Urban", "Semiurban", "Rural"],
    "Credit_History": [0.0, 1.0],
}

NUMERIC_RANGES = {
    "ApplicantIncome": (0, 100000),
    "CoapplicantIncome": (0, 100000),
    "LoanAmount": (0, 1000),
    "Loan_Amount_Term": (0, 600),
    "Credit_History": (0, 1),
}