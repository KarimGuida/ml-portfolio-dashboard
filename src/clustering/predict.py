import pandas as pd

from src.utils.helpers import load_object

MODEL_PATH = "models/clustering_model.pkl"
SCALER_PATH = "models/clustering_scaler.pkl"


def predict_cluster(income, score):
    model = load_object(MODEL_PATH)
    scaler = load_object(SCALER_PATH)

    df = pd.DataFrame(
        [[income, score]],
        columns=["Annual_Income", "Spending_Score"]
    )

    scaled = scaler.transform(df)
    cluster = model.predict(scaled)[0]

    return int(cluster)