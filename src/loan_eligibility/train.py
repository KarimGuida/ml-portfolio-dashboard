import json
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier

from src.loan_eligibility.schema import (
    FEATURE_COLUMNS,
    TARGET_COLUMN,
    DROP_COLUMNS,
    CATEGORICAL_COLUMNS,
    NUMERICAL_COLUMNS,
)
from src.utils.helpers import save_object


DATA_PATH = "data/credit.csv"
MODEL_PATH = "models/loan_eligibility_pipeline.pkl"
LABEL_ENCODER_PATH = "models/loan_eligibility_label_encoder.pkl"
METRICS_PATH = "models/loan_eligibility_metrics.json"


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df = df.drop(columns=DROP_COLUMNS, errors="ignore")
    return df


def build_pipeline():
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, NUMERICAL_COLUMNS),
            ("cat", categorical_transformer, CATEGORICAL_COLUMNS),
        ]
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", RandomForestClassifier(n_estimators=200, random_state=42)),
        ]
    )

    return pipeline


def main():
    df = load_data()

    X = df[FEATURE_COLUMNS].copy()
    y = df[TARGET_COLUMN].copy()

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y_encoded,
        test_size=0.2,
        random_state=42,
        stratify=y_encoded,
    )

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred).tolist()
    report = classification_report(y_test, y_pred, output_dict=True)

    save_object(pipeline, MODEL_PATH)
    save_object(label_encoder, LABEL_ENCODER_PATH)

    metrics = {
        "accuracy": round(float(accuracy), 4),
        "confusion_matrix": cm,
        "classification_report": report,
        "train_shape": list(X_train.shape),
        "test_shape": list(X_test.shape),
    }

    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=4)

    print(f"Accuracy: {accuracy:.4f}")
    print(f"Saved pipeline to: {MODEL_PATH}")
    print(f"Saved label encoder to: {LABEL_ENCODER_PATH}")
    print(f"Saved metrics to: {METRICS_PATH}")


if __name__ == "__main__":
    main()