import pandas as pd

from src.utils.helpers import load_object

MODEL_PATH = "models/neural_network_pipeline.pkl"


def predict_admission(input_data: dict):
    model = load_object(MODEL_PATH)

    df = pd.DataFrame([input_data])

    predicted_class = int(model.predict(df)[0])

    if hasattr(model, "predict_proba"):
        probability = float(model.predict_proba(df)[0][1])
    else:
        probability = None

    return {
        "predicted_class": predicted_class,
        "probability": probability
    }