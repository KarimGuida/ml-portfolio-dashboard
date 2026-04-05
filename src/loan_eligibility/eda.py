import pandas as pd

from src.loan_eligibility.schema import TARGET_COLUMN, DROP_COLUMNS


DATA_PATH = "data/credit.csv"


def load_raw_data() -> pd.DataFrame:
    return pd.read_csv(DATA_PATH)


def get_dataset_summary(df: pd.DataFrame) -> dict:
    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
    }


def get_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    missing = df.isnull().sum().reset_index()
    missing.columns = ["Feature", "MissingCount"]
    missing["MissingPercent"] = (missing["MissingCount"] / len(df) * 100).round(2)
    return missing.sort_values(by="MissingCount", ascending=False)


def get_numeric_summary(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    return df[numeric_cols].describe().T


def get_target_distribution(df: pd.DataFrame) -> pd.DataFrame:
    dist = df[TARGET_COLUMN].value_counts(dropna=False).reset_index()
    dist.columns = ["Loan_Approved", "Count"]
    return dist


def get_approval_by_category(df: pd.DataFrame, category_col: str) -> pd.DataFrame:
    temp = (
        df.groupby([category_col, TARGET_COLUMN])
        .size()
        .reset_index(name="Count")
        .sort_values(by=[category_col, TARGET_COLUMN])
    )
    return temp


def get_clean_feature_frame(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(columns=DROP_COLUMNS, errors="ignore").copy()