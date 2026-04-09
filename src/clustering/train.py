import pandas as pd
import json

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from src.logging_config import get_logger
from src.utils.helpers import save_object

logger = get_logger(__name__)

DATA_PATH = "data/mall_customers.csv"
MODEL_PATH = "models/clustering_model.pkl"
SCALER_PATH = "models/clustering_scaler.pkl"
METRICS_PATH = "models/clustering_metrics.json"


def load_data():
    logger.info("Loading dataset from %s", DATA_PATH)
    df = pd.read_csv(DATA_PATH)
    logger.info("Dataset loaded successfully with shape=%s", df.shape)
    return df


def main():
    logger.info("Starting clustering training pipeline")

    try:
        df = load_data()

        feature_columns = ["Annual_Income", "Spending_Score"]
        logger.info("Selected features: %s", feature_columns)

        X = df[feature_columns].copy()

        logger.info("Applying StandardScaler to features")
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        logger.info("Training KMeans model with n_clusters=5")
        kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
        kmeans.fit(X_scaled)

        logger.info("Saving model to %s", MODEL_PATH)
        save_object(kmeans, MODEL_PATH)

        logger.info("Saving scaler to %s", SCALER_PATH)
        save_object(scaler, SCALER_PATH)

        metrics = {
            "n_clusters": 5,
            "features": feature_columns,
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
        }

        logger.info("Saving metrics to %s", METRICS_PATH)
        with open(METRICS_PATH, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=4)

        logger.info("Clustering training completed successfully")
        logger.info("Metrics: %s", metrics)

    except Exception:
        logger.exception("Error during clustering training pipeline")
        raise


if __name__ == "__main__":
    main()