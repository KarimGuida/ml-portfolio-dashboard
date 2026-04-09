import pandas as pd

from src.utils.helpers import load_object
from src.logging_config import get_logger

logger = get_logger(__name__)

MODEL_PATH = "models/clustering_model.pkl"
SCALER_PATH = "models/clustering_scaler.pkl"


def predict_cluster(income, score):
    logger.info(
        "Starting clustering inference with Annual_Income=%s, Spending_Score=%s",
        income,
        score,
    )

    try:
        logger.info("Loading clustering model from %s", MODEL_PATH)
        model = load_object(MODEL_PATH)

        logger.info("Loading clustering scaler from %s", SCALER_PATH)
        scaler = load_object(SCALER_PATH)

        df = pd.DataFrame(
            [[income, score]],
            columns=["Annual_Income", "Spending_Score"]
        )

        logger.info("Applying scaler transformation")
        scaled = scaler.transform(df)

        logger.info("Predicting cluster")
        cluster = model.predict(scaled)[0]

        logger.info("Prediction successful: cluster=%s", cluster)

        return int(cluster)

    except Exception:
        logger.exception("Error during clustering prediction")
        raise