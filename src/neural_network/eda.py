import pandas as pd

DATA_PATH = "data/Admission.csv"


def load_data():
    return pd.read_csv(DATA_PATH)


def summary(df):
    return {
        "rows": df.shape[0],
        "cols": df.shape[1],
        "missing": int(df.isnull().sum().sum())
    }


def numeric_summary(df):
    return df.describe().T