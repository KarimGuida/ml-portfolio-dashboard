import matplotlib.pyplot as plt
import pandas as pd


def get_cluster_labels(centers):
    labels = []

    for income, score in centers:
        if income >= 85 and score >= 65:
            labels.append("High Income / High Spending")
        elif income >= 85 and score < 40:
            labels.append("High Income / Low Spending")
        elif income < 45 and score >= 65:
            labels.append("Low Income / High Spending")
        elif income < 45 and score < 40:
            labels.append("Low Income / Low Spending")
        else:
            labels.append("Average Customers")

    return labels


def get_cluster_legend_df(model, scaler):
    centers_scaled = model.cluster_centers_
    centers = scaler.inverse_transform(centers_scaled)
    labels = get_cluster_labels(centers)

    rows = []
    for i, (center, label) in enumerate(zip(centers, labels)):
        rows.append(
            {
                "Cluster": i,
                "Segment Label": label,
                "Center Income": round(float(center[0]), 2),
                "Center Spending Score": round(float(center[1]), 2),
            }
        )

    return pd.DataFrame(rows)


def plot_clusters(df, model, scaler, user_point=None):
    X = df[["Annual_Income", "Spending_Score"]]
    X_scaled = scaler.transform(X)
    clusters = model.predict(X_scaled)

    fig, ax = plt.subplots(figsize=(10, 7))

    ax.scatter(
        X["Annual_Income"],
        X["Spending_Score"],
        c=clusters,
        alpha=0.7,
        s=60
    )

    centers_scaled = model.cluster_centers_
    centers = scaler.inverse_transform(centers_scaled)

    ax.scatter(
        centers[:, 0],
        centers[:, 1],
        marker="X",
        s=280,
        linewidths=2,
        label="Cluster Centers"
    )

    # Put cluster numbers on the centers
    for i, (x, y) in enumerate(centers):
        ax.annotate(
            str(i),
            (x, y),
            xytext=(0, 0),
            textcoords="offset points",
            ha="center",
            va="center",
            fontsize=11,
            fontweight="bold"
        )

    if user_point is not None:
        ax.scatter(
            user_point[0],
            user_point[1],
            marker="*",
            s=320,
            label="Your Input"
        )

    ax.set_xlabel("Annual Income")
    ax.set_ylabel("Spending Score")
    ax.set_title("Customer Segments")
    ax.legend()
    fig.tight_layout()

    return fig