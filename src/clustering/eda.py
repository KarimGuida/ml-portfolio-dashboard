import pandas as pd


DATA_PATH = "data/mall_customers.csv"


def load_clustering_data(path: str = DATA_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def get_dataset_preview(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    return df.head(n)


def get_summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    return df.describe()


def get_feature_view(df: pd.DataFrame) -> pd.DataFrame:
    return df[["Annual_Income", "Spending_Score"]].copy()


def get_eda_observations() -> list[str]:
    return [
        "Customer behavior can be interpreted through the relationship between annual income and spending score.",
        "Customers with similar income levels may still show very different spending patterns.",
        "The distribution suggests the presence of distinct behavioral groups rather than a single uniform customer base.",
        "These patterns support the use of clustering to identify interpretable customer segments.",
    ]