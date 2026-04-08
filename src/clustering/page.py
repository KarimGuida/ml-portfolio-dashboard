import streamlit as st
import pandas as pd

from src.clustering.predict import predict_cluster
from src.clustering.eda import (
    load_clustering_data,
    get_dataset_preview,
    get_summary_statistics,
    get_feature_view,
    get_eda_observations,
)
from src.utils.helpers import load_object
from src.clustering.visuals import (
    plot_clusters,
    get_cluster_legend_df,
)

MODEL_PATH = "models/clustering_model.pkl"
SCALER_PATH = "models/clustering_scaler.pkl"


def render_clustering_page():
    st.header("Customer Segmentation")
    st.write("Segment customers into behavior-based groups using a K-Means clustering model.")

    tabs = st.tabs(["Overview", "EDA", "Model", "Predict"])

    df = load_clustering_data()
    feature_df = get_feature_view(df)

    model = load_object(MODEL_PATH)
    scaler = load_object(SCALER_PATH)
    legend_df = get_cluster_legend_df(model, scaler)

    with tabs[0]:
        st.subheader("Overview")
        st.markdown(
            """
            This module applies **K-Means clustering** to group customers based on behavioral attributes.

            **Business objective**
            - Identify distinct customer segments
            - Support targeted marketing strategies
            - Improve interpretation of spending behavior

            **Features used in deployed model**
            - Annual Income
            - Spending Score
            """
        )

        st.markdown("### Dataset Preview")
        st.dataframe(get_dataset_preview(df), width="stretch")

    with tabs[1]:
        st.subheader("Exploratory Data Analysis")

        st.markdown("### Income vs Spending Score")
        st.scatter_chart(
            feature_df,
            x="Annual_Income",
            y="Spending_Score",
        )

        st.markdown("### Summary Statistics")
        st.dataframe(get_summary_statistics(feature_df), width="stretch")

        st.markdown("### Key Observations")
        for obs in get_eda_observations():
            st.write(f"- {obs}")

    with tabs[2]:
        st.subheader("Model Output")
        st.write(
            "The deployed model partitions customers into five segments using standardized income and spending features."
        )

        st.pyplot(plot_clusters(df, model, scaler))
        st.caption("Numbers on the X markers identify the cluster centers.")

        st.markdown("### Cluster Segment Reference")
        st.dataframe(legend_df, width="stretch")

        st.markdown("### Model Interpretation")
        st.write(
            """
            Cluster centers represent the average profile of each customer group.
            Segment labels are assigned by interpreting the relative position of each cluster center
            in terms of income and spending behavior.
            """
        )

    with tabs[3]:
        st.subheader("Interactive Prediction")
        st.write("Enter customer values to identify the most likely segment.")

        col1, col2 = st.columns(2)

        with col1:
            income = st.slider(
                "Annual Income",
                min_value=int(df["Annual_Income"].min()),
                max_value=int(df["Annual_Income"].max()),
                value=60,
                help="Customer annual income",
            )

        with col2:
            score = st.slider(
                "Spending Score",
                min_value=int(df["Spending_Score"].min()),
                max_value=int(df["Spending_Score"].max()),
                value=50,
                help="Customer spending behavior score",
            )

        if st.button("Predict"):
            try:
                cluster = predict_cluster(income, score)
                segment_label = legend_df.loc[
                    legend_df["Cluster"] == cluster, "Segment Label"
                ].iloc[0]

                st.markdown("### Prediction Result")
                st.success(f"Assigned Segment: Cluster {cluster} — {segment_label}")

                st.markdown("### Position in Cluster Map")
                st.pyplot(plot_clusters(df, model, scaler, user_point=(income, score)))

                st.markdown("### Segment Reference")
                st.dataframe(legend_df, width="stretch")

                st.markdown("### Input Summary")
                input_summary = pd.DataFrame(
                    [{
                        "Annual_Income": income,
                        "Spending_Score": score,
                    }]
                )
                st.dataframe(input_summary, width="stretch")

            except Exception as e:
                st.error(f"Error: {e}")