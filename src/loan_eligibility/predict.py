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
from src.logging_config import get_logger

logger = get_logger(__name__)

MODEL_PATH = "models/loan_eligibility_pipeline.pkl"
LABEL_ENCODER_PATH = "models/loan_eligibility_label_encoder.pkl"


def predict_loan_eligibility(input_data: dict) -> dict:
    logger.info("Starting loan eligibility inference")

    try:
        logger.info("Validating required fields")
        validate_required_fields(input_data, FEATURE_COLUMNS)

        logger.info("Validating categorical values")
        validate_allowed_values(input_data, ALLOWED_VALUES)

        logger.info("Validating numeric ranges")
        validate_numeric_ranges(input_data, NUMERIC_RANGES)

        logger.info("Loading prediction pipeline from %s", MODEL_PATH)
        model = load_object(MODEL_PATH)

        logger.info("Loading label encoder from %s", LABEL_ENCODER_PATH)
        label_encoder = load_object(LABEL_ENCODER_PATH)

        logger.info("Converting input data to dataframe")
        input_df = convert_input_to_dataframe(input_data, FEATURE_COLUMNS)

        logger.info("Running prediction")
        prediction_encoded = model.predict(input_df)[0]
        prediction_label = label_encoder.inverse_transform([prediction_encoded])[0]

        confidence = None
        if hasattr(model, "predict_proba"):
            logger.info("Computing prediction confidence")
            probabilities = model.predict_proba(input_df)[0]
            confidence = float(max(probabilities))

        logger.info(
            "Loan eligibility prediction successful: prediction=%s, confidence=%s",
            prediction_label,
            confidence,
        )

        return {
            "prediction": prediction_label,
            "confidence": confidence,
        }

    except Exception:
        logger.exception("Error during loan eligibility inference")
        raise