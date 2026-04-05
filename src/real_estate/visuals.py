import matplotlib.pyplot as plt


def plot_price_distribution(df):
    fig, ax = plt.subplots()
    df["price"].hist(bins=30, ax=ax)
    ax.set_title("Price Distribution")
    return fig


def plot_scatter(df, col):
    fig, ax = plt.subplots()
    ax.scatter(df[col], df["price"])
    ax.set_title(f"{col} vs Price")
    return fig