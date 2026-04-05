from src.loan_eligibility.schema import (
    FEATURE_COLUMNS,
    ALLOWED_VALUES,
    NUMERIC_RANGES,
)
from src.utils.validators import (
    validate_required_fields,
    validate_allowed_values,
    validate_numeric_ranges,
    convert_input_to_dataframe,
)
from src.utils.helpers import load_object


MODEL_PATH = "models/loan_eligibility_pipeline.pkl"
LABEL_ENCODER_PATH = "models/loan_eligibility_label_encoder.pkl"


def predict_loan_eligibility(input_data: dict) -> dict:
    validate_required_fields(input_data, FEATURE_COLUMNS)
    validate_allowed_values(input_data, ALLOWED_VALUES)
    validate_numeric_ranges(input_data, NUMERIC_RANGES)

    model = load_object(MODEL_PATH)
    label_encoder = load_object(LABEL_ENCODER_PATH)

    input_df = convert_input_to_dataframe(input_data, FEATURE_COLUMNS)

    prediction_encoded = model.predict(input_df)[0]
    prediction_label = label_encoder.inverse_transform([prediction_encoded])[0]

    confidence = None
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(input_df)[0]
        confidence = float(max(probabilities))

    return {
        "prediction": prediction_label,
        "confidence": confidence,
    }