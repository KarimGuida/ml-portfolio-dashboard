import pandas as pd

from src.utils.helpers import load_object

MODEL_PATH = "models/neural_network_pipeline.pkl"


def predict_admission(input_data: dict):
    model = load_object(MODEL_PATH)

    df = pd.DataFrame([input_data])

    prediction = model.predict(df)[0]

    prediction = max(0.0, min(1.0, float(prediction)))

    return round(prediction, 4)