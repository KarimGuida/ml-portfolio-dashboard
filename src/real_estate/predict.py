import pandas as pd

from src.utils.helpers import load_object
from src.logging_config import get_logger

logger = get_logger(__name__)

MODEL_PATH = "models/real_estate_pipeline.pkl"


def predict_price(input_data: dict):
    logger.info("Starting real estate inference")

    try:
        logger.info("Loading model from %s", MODEL_PATH)
        model = load_object(MODEL_PATH)

        logger.info("Converting input data to dataframe")
        df = pd.DataFrame([input_data])

        logger.info("Running prediction")
        prediction = model.predict(df)[0]

        price = round(float(prediction), 2)

        logger.info("Prediction successful: price=%s", price)

        return price

    except Exception:
        logger.exception("Error during real estate inference")
        raise