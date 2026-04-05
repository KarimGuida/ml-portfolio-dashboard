import pandas as pd
import json

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from src.utils.helpers import save_object

DATA_PATH = "data/mall_customers.csv"
MODEL_PATH = "models/clustering_model.pkl"
SCALER_PATH = "models/clustering_scaler.pkl"
METRICS_PATH = "models/clustering_metrics.json"


def load_data():
    return pd.read_csv(DATA_PATH)


def main():
    df = load_data()

    feature_columns = ["Annual_Income", "Spending_Score"]
    X = df[feature_columns].copy()

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    kmeans.fit(X_scaled)

    save_object(kmeans, MODEL_PATH)
    save_object(scaler, SCALER_PATH)

    metrics = {
        "n_clusters": 5,
        "features": feature_columns,
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
    }

    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=4)

    print("Clustering model saved successfully.")
    print(metrics)


if __name__ == "__main__":
    main()