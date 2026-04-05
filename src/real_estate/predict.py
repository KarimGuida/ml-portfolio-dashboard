import pandas as pd

from src.utils.helpers import load_object

MODEL_PATH = "models/real_estate_pipeline.pkl"


def predict_price(input_data: dict):
    model = load_object(MODEL_PATH)

    df = pd.DataFrame([input_data])

    prediction = model.predict(df)[0]

    return round(float(prediction), 2)