import streamlit as st


def render_home_page() -> None:
    st.markdown("""
        <div class="hero-wrap">
        <div class="hero-kicker">Machine Learning Project</div>
        <div class="hero-title">Machine Learning Dashboard</div>
        <div class="hero-subtitle">
            A modular machine learning system designed to simulate real-world data science workflows,
            including model development, evaluation, and deployment-ready interactive applications.
        </div>
        </div>
""", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Projects", "4")
    c2.metric("Models", "4")
    c3.metric("Architecture", "Modular")
    c4.metric("Deployment", "Streamlit")

    st.markdown('<div class="section-title">Included Projects</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="project-card">
                <div class="project-title">💳 Loan Eligibility Prediction</div>
                <div class="project-badge">Classification</div>
                <div class="small-note">
                    Binary classification model designed to assess loan approval risk based on applicant financial and demographic features.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="project-card">
                <div class="project-title">🏠 Real Estate Price Prediction</div>
                <div class="project-badge">Regression</div>
                <div class="small-note">
                    Regression model developed to estimate property values using structured housing features and market-related indicators.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="project-card">
                <div class="project-title">👥 Customer Segmentation</div>
                <div class="project-badge">Clustering</div>
                <div class="small-note">
                    Unsupervised clustering model used to identify distinct customer segments based on income and spending behavior for targeted analysis.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="project-card">
                <div class="project-title">🎓 Admission Prediction with Neural Network</div>
                <div class="project-badge">MLPRegressor</div>
                <div class="small-note">
                    Neural network regression model used to estimate admission likelihood based on academic performance and applicant profile features.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-title">Technical Highlights</div>', unsafe_allow_html=True)

    st.markdown("""
<div class="tech-list">
<ul>
<li>Modular Python architecture separating data processing, modeling, and UI layers</li>
<li>Model persistence using serialized artifacts for reproducible inference</li>
<li>End-to-end ML workflow: data preparation, model training, evaluation, and deployment</li>
<li>Interactive dashboard enabling real-time predictions and model exploration</li>
<li>Scalable design allowing integration of additional machine learning use cases</li>
</ul>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="highlight-box">
<strong>Key Value:</strong><br><br>
This project demonstrates the transition from isolated analytical workflows to a unified,
production-style machine learning system. It emphasizes modular design, reproducibility,
and the ability to operationalize models through interactive applications.
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="footer-note">
Explore each module to interact with deployed models and evaluate their behavior across different scenarios.
</div>
""", unsafe_allow_html=True)