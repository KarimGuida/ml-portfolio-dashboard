import streamlit as st


def render_home_page() -> None:
    st.markdown(
        """
        <div class="hero-wrap">
            <div class="hero-kicker">Portfolio • Streamlit • Modular ML</div>
            <div class="hero-title">📊 ML Final Project Portfolio</div>
            <div class="hero-subtitle">
                A modern machine learning application that transforms four separate notebook projects
                into one polished, deployable, and reusable portfolio dashboard.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

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
                    Predict whether a loan application is likely to be approved using applicant profile,
                    credit history, and financial indicators.
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
                    Estimate property sale prices using structured housing features such as square footage,
                    tax, lot size, year built, and other property indicators.
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
                    Group customers into behavioral segments using annual income and spending score,
                    with interactive cluster exploration.
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
                    Estimate graduate admission probability using GRE, TOEFL, CGPA, SOP, LOR,
                    university rating, and research experience.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-title">Technical Highlights</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="tech-list">
            <ul>
                <li>Modular Python structure with separate modules for training, prediction, EDA, and visuals</li>
                <li>Saved model artifacts using <code>.pkl</code> files for deployment-ready inference</li>
                <li>Interactive Streamlit pages with model metrics, forms, and visual analysis</li>
                <li>Consistent UI for portfolio presentation and classroom demonstration</li>
                <li>Reusable architecture suitable for future ML app extensions</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="highlight-box">
            <strong>Why this stands out:</strong><br>
            Instead of presenting four disconnected notebooks, this app integrates them into one
            professional, modern, and maintainable machine learning portfolio.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="footer-note">
            Use the navigation on the left to explore each project and test the interactive features.
        </div>
        """,
        unsafe_allow_html=True,
    )