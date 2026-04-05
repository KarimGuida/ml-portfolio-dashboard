import matplotlib.pyplot as plt


def plot_target_distribution(df):
    fig, ax = plt.subplots()
    df["Admit_Chance"].hist(bins=30, ax=ax)
    ax.set_title("Admit Chance Distribution")
    ax.set_xlabel("Admit Chance")
    ax.set_ylabel("Frequency")
    return fig


def plot_scatter(df, col):
    fig, ax = plt.subplots()
    ax.scatter(df[col], df["Admit_Chance"], alpha=0.7)
    ax.set_title(f"{col} vs Admit Chance")
    ax.set_xlabel(col)
    ax.set_ylabel("Admit Chance")
    return fig