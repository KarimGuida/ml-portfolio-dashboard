import json
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier

from src.logging_config import get_logger
from src.loan_eligibility.schema import (
    FEATURE_COLUMNS,
    TARGET_COLUMN,
    DROP_COLUMNS,
    CATEGORICAL_COLUMNS,
    NUMERICAL_COLUMNS,
)
from src.utils.helpers import save_object

logger = get_logger(__name__)

DATA_PATH = "data/credit.csv"
MODEL_PATH = "models/loan_eligibility_pipeline.pkl"
LABEL_ENCODER_PATH = "models/loan_eligibility_label_encoder.pkl"
METRICS_PATH = "models/loan_eligibility_metrics.json"


def load_data() -> pd.DataFrame:
    logger.info("Loading loan eligibility dataset from %s", DATA_PATH)
    df = pd.read_csv(DATA_PATH)
    df = df.drop(columns=DROP_COLUMNS, errors="ignore")
    logger.info("Dataset loaded successfully with shape=%s", df.shape)
    return df


def build_pipeline():
    logger.info("Building preprocessing and classification pipeline")

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

    logger.info("Pipeline built successfully")
    return pipeline


def main():
    logger.info("Starting loan eligibility training pipeline")

    try:
        df = load_data()

        logger.info("Preparing features and target")
        X = df[FEATURE_COLUMNS].copy()
        y = df[TARGET_COLUMN].copy()

        logger.info("Encoding target labels")
        label_encoder = LabelEncoder()
        y_encoded = label_encoder.fit_transform(y)

        logger.info("Splitting dataset into train and test sets")
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y_encoded,
            test_size=0.2,
            random_state=42,
            stratify=y_encoded,
        )
        logger.info(
            "Train/test split complete with train_shape=%s and test_shape=%s",
            X_train.shape,
            X_test.shape,
        )

        pipeline = build_pipeline()

        logger.info("Training RandomForestClassifier pipeline")
        pipeline.fit(X_train, y_train)

        logger.info("Evaluating model on test set")
        y_pred = pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred).tolist()
        report = classification_report(y_test, y_pred, output_dict=True)

        logger.info("Saving trained pipeline to %s", MODEL_PATH)
        save_object(pipeline, MODEL_PATH)

        logger.info("Saving label encoder to %s", LABEL_ENCODER_PATH)
        save_object(label_encoder, LABEL_ENCODER_PATH)

        metrics = {
            "accuracy": round(float(accuracy), 4),
            "confusion_matrix": cm,
            "classification_report": report,
            "train_shape": list(X_train.shape),
            "test_shape": list(X_test.shape),
        }

        logger.info("Saving evaluation metrics to %s", METRICS_PATH)
        with open(METRICS_PATH, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=4)

        logger.info("Loan eligibility training completed successfully")
        logger.info("Final accuracy: %.4f", accuracy)

    except Exception:
        logger.exception("Error during loan eligibility training pipeline")
        raise


if __name__ == "__main__":
    main()