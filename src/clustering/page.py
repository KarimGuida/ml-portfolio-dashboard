import streamlit as st
import pandas as pd

from src.clustering.predict import predict_cluster
from src.utils.helpers import load_object
from src.clustering.visuals import (
    plot_clusters,
    get_cluster_legend_df,
)

MODEL_PATH = "models/clustering_model.pkl"
SCALER_PATH = "models/clustering_scaler.pkl"
DATA_PATH = "data/mall_customers.csv"


def render_clustering_page():
    st.header("Customer Segmentation (Clustering)")
    st.write("Segment customers based on income and spending behavior.")

    tabs = st.tabs(["Overview", "EDA", "Model", "Predict"])

    df = pd.read_csv(DATA_PATH)

    model = load_object(MODEL_PATH)
    scaler = load_object(SCALER_PATH)
    legend_df = get_cluster_legend_df(model, scaler)

    with tabs[0]:
        st.subheader("Project Overview")
        st.markdown(
            """
            This project uses **K-Means clustering** to segment customers based on:

            - Annual Income
            - Spending Score

            Each cluster represents a different customer group with similar behavior.
            """
        )

        
        c1, c2, c3 = st.columns(3)
        c1.metric("Rows", df.shape[0])
        c2.metric("Columns", df.shape[1])
        c3.metric("Clusters", 5)
        st.subheader("Dataset Preview")
        st.dataframe(df.head(10), width="stretch")

        
    with tabs[1]:
        st.subheader("Exploratory Data Analysis")

        st.markdown("### Income vs Spending Score")
        st.scatter_chart(
            df,
            x="Annual_Income",
            y="Spending_Score"
        )

        st.markdown("### Summary Statistics")
        st.dataframe(df.describe(), width="stretch")

    with tabs[2]:
        st.subheader("Model Output")
        st.pyplot(plot_clusters(df, model, scaler))
        st.caption("Numbers on the X markers identify the cluster centers.")

        st.markdown("### Cluster Segment Labels")
        st.dataframe(legend_df, width="stretch")

    with tabs[3]:
        st.subheader("Interactive Prediction")
        st.write(
            "Adjust the values below to see which customer segment a profile belongs to."
        )

        col1, col2 = st.columns(2)

        with col1:
            income = st.slider(
                "Annual Income",
                min_value=int(df["Annual_Income"].min()),
                max_value=int(df["Annual_Income"].max()),
                value=60,
                help="Customer annual income"
            )

        with col2:
            score = st.slider(
                "Spending Score",
                min_value=int(df["Spending_Score"].min()),
                max_value=int(df["Spending_Score"].max()),
                value=50,
                help="Customer spending behavior score"
            )

        if st.button("Assign Cluster"):
            try:
                cluster = predict_cluster(income, score)
                segment_label = legend_df.loc[
                    legend_df["Cluster"] == cluster, "Segment Label"
                ].iloc[0]

                st.success(f"Customer belongs to Cluster {cluster}: {segment_label}")

                st.markdown("### Your Position in the Cluster Map")
                st.pyplot(plot_clusters(df, model, scaler, user_point=(income, score)))

                st.markdown("### Cluster Segment Labels")
                st.dataframe(legend_df, width="stretch")

                st.markdown("### Input Summary")
                st.json({
                    "Annual_Income": income,
                    "Spending_Score": score
                })

            except Exception as e:
                st.error(f"Error: {e}")