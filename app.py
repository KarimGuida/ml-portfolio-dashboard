import streamlit as st

from src.styles import apply_global_styles
from src.home import render_home_page
from src.loan_eligibility.page import render_loan_eligibility_page
from src.real_estate.page import render_real_estate_page
from src.clustering.page import render_clustering_page
from src.neural_network.page import render_neural_network_page

st.set_page_config(
    page_title="Enterprise ML Portfolio",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_global_styles()

PAGES = {
    "Home": render_home_page,
    "Loan Eligibility": render_loan_eligibility_page,
    "Real Estate": render_real_estate_page,
    "Customer Segmentation": render_clustering_page,
    "Admission Prediction": render_neural_network_page,
}

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-kicker">Portfolio Dashboard</div>
            <div class="sidebar-brand-title">Enterprise ML Portfolio</div>
            <div class="sidebar-brand-subtitle">
                Modular machine learning applications with a unified interface.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-label">Navigation</div>', unsafe_allow_html=True)

    page = st.radio(
        "Go to",
        list(PAGES.keys()),
        index=0,
        key="main_project_radio",
        label_visibility="collapsed",
    )

    st.markdown(
        """
        <div class="sidebar-footer">
            Built with Streamlit • Modular Python • Saved ML pipelines
        </div>
        """,
        unsafe_allow_html=True,
    )

PAGES[page]()