import pandas as pd
import json

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from src.logging_config import get_logger
from src.utils.helpers import save_object

logger = get_logger(__name__)

DATA_PATH = "data/final.csv"
MODEL_PATH = "models/real_estate_pipeline.pkl"
METRICS_PATH = "models/real_estate_metrics.json"


def load_data():
    logger.info("Loading real estate dataset from %s", DATA_PATH)
    df = pd.read_csv(DATA_PATH)
    logger.info("Dataset loaded successfully with shape=%s", df.shape)
    return df


def main():
    logger.info("Starting real estate training pipeline")

    try:
        df = load_data()

        logger.info("Dropping rows with missing target values in 'price'")
        df = df.dropna(subset=["price"])
        logger.info("Dataset shape after target filtering: %s", df.shape)

        logger.info("Preparing features and target")
        X = df.drop(columns=["price"])
        y = df["price"]

        numeric_cols = X.select_dtypes(include=["number"]).columns.tolist()
        categorical_cols = X.select_dtypes(exclude=["number"]).columns.tolist()

        logger.info("Numeric columns: %s", numeric_cols)
        logger.info("Categorical columns: %s", categorical_cols)

        logger.info("Building preprocessing pipelines")
        numeric_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ])

        categorical_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent"))
        ])

        preprocessor = ColumnTransformer([
            ("num", numeric_pipeline, numeric_cols),
            ("cat", categorical_pipeline, categorical_cols)
        ])

        logger.info("Building RandomForestRegressor pipeline")
        pipeline = Pipeline([
            ("preprocessor", preprocessor),
            ("model", RandomForestRegressor(n_estimators=200, random_state=42))
        ])

        logger.info("Splitting dataset into train and test sets")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        logger.info(
            "Train/test split complete with train_shape=%s and test_shape=%s",
            X_train.shape,
            X_test.shape,
        )

        logger.info("Training regression pipeline")
        pipeline.fit(X_train, y_train)

        logger.info("Evaluating model on test set")
        y_pred = pipeline.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)
        rmse = mean_squared_error(y_test, y_pred) ** 0.5
        r2 = r2_score(y_test, y_pred)

        logger.info("Saving trained pipeline to %s", MODEL_PATH)
        save_object(pipeline, MODEL_PATH)

        metrics = {
            "MAE": float(mae),
            "RMSE": float(rmse),
            "R2": float(r2),
            "train_shape": list(X_train.shape),
            "test_shape": list(X_test.shape),
            "features": list(X.columns)
        }

        logger.info("Saving metrics to %s", METRICS_PATH)
        with open(METRICS_PATH, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=4)

        logger.info("Real estate training completed successfully")
        logger.info("Final metrics: %s", metrics)

    except Exception:
        logger.exception("Error during real estate training pipeline")
        raise


if __name__ == "__main__":
    main()