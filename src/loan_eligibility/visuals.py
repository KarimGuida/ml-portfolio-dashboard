import matplotlib.pyplot as plt
import pandas as pd


def plot_target_distribution(target_df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(target_df["Loan_Approved"], target_df["Count"])
    ax.set_title("Loan Approval Distribution")
    ax.set_xlabel("Loan Approved")
    ax.set_ylabel("Count")
    return fig


def plot_loan_amount_distribution(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(7, 4))
    df["LoanAmount"].dropna().plot(kind="hist", bins=30, ax=ax)
    ax.set_title("Loan Amount Distribution")
    ax.set_xlabel("Loan Amount")
    ax.set_ylabel("Frequency")
    return fig


def plot_applicant_income_distribution(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(7, 4))
    df["ApplicantIncome"].dropna().plot(kind="hist", bins=30, ax=ax)
    ax.set_title("Applicant Income Distribution")
    ax.set_xlabel("Applicant Income")
    ax.set_ylabel("Frequency")
    return fig


def plot_approval_by_category(cat_df: pd.DataFrame, category_col: str):
    pivot_df = cat_df.pivot(index=category_col, columns="Loan_Approved", values="Count").fillna(0)

    fig, ax = plt.subplots(figsize=(7, 4))
    pivot_df.plot(kind="bar", ax=ax)
    ax.set_title(f"Loan Approval by {category_col}")
    ax.set_xlabel(category_col)
    ax.set_ylabel("Count")
    ax.legend(title="Loan Approved")
    return fig


def plot_correlation_heatmap(df: pd.DataFrame):
    numeric_df = df.select_dtypes(include=["number"]).copy()
    corr = numeric_df.corr()

    fig, ax = plt.subplots(figsize=(7, 5))
    im = ax.imshow(corr, aspect="auto")
    ax.set_xticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(corr.columns)))
    ax.set_yticklabels(corr.columns)
    ax.set_title("Correlation Heatmap (Numeric Features)")
    fig.colorbar(im, ax=ax)
    return fig