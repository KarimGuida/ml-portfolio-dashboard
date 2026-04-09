import pandas as pd

from src.utils.helpers import load_object
from src.logging_config import get_logger

logger = get_logger(__name__)

MODEL_PATH = "models/neural_network_pipeline.pkl"


def predict_admission(input_data: dict):
    logger.info("Starting neural network inference")

    try:
        logger.info("Loading model from %s", MODEL_PATH)
        model = load_object(MODEL_PATH)

        logger.info("Converting input data to dataframe")
        df = pd.DataFrame([input_data])

        logger.info("Running prediction")
        predicted_class = int(model.predict(df)[0])

        probability = None
        if hasattr(model, "predict_proba"):
            logger.info("Computing prediction probability")
            probability = float(model.predict_proba(df)[0][1])

        logger.info(
            "Prediction successful: class=%s, probability=%s",
            predicted_class,
            probability,
        )

        return {
            "predicted_class": predicted_class,
            "probability": probability
        }

    except Exception:
        logger.exception("Error during neural network inference")
        raise