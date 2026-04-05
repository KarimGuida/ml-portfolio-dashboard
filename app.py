import streamlit as st

from src.styles import apply_global_styles
from src.home import render_home_page
from src.loan_eligibility.page import render_loan_eligibility_page
from src.real_estate.page import render_real_estate_page
from src.clustering.page import render_clustering_page
from src.neural_network.page import render_neural_network_page

st.set_page_config(
    page_title="ML Final Project",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_global_styles()

with st.sidebar:
    st.markdown("## Navigation")
    page = st.radio(
        "Choose a page",
        ["Home", "Loan Eligibility", "Real Estate", "Clustering", "Neural Network"],
        index=0,
        key="main_project_radio",
    )

if page == "Home":
    render_home_page()
elif page == "Loan Eligibility":
    render_loan_eligibility_page()
elif page == "Real Estate":
    render_real_estate_page()
elif page == "Clustering":
    render_clustering_page()
elif page == "Neural Network":
    render_neural_network_page()