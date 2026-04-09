# ML Portfolio Dashboard

A modular, production-style machine learning portfolio built with **Streamlit**, showcasing multiple end-to-end ML projects including classification, regression, clustering, and neural networks.

try the app: https://ml-portfolio-dashboard.streamlit.app/

---

## Overview

This application integrates four machine learning workflows into a single interactive dashboard:

- ✔️ Clean UI with modern styling  
- ✔️ Modular architecture (training, prediction, EDA separated)  
- ✔️ Interactive inputs for real-time predictions  
- ✔️ Visualization and interpretation of model outputs  

---

## Projects Included

### 1. Loan Eligibility Prediction
- **Type:** Classification  
- **Model:** Random Forest  
- **Goal:** Predict whether a loan application will be approved  

**Features:**
- Applicant income  
- Credit history  
- Education  
- Loan amount  
- Property area  

---

### 2. Real Estate Price Prediction
- **Type:** Regression  
- **Model:** Random Forest Regressor  
- **Goal:** Estimate property prices  

**Features:**
- Square footage  
- Number of bedrooms/bathrooms  
- Property tax & insurance  
- Year built  
- Lot size  

---

### 3. Customer Segmentation (Clustering)
- **Type:** Unsupervised Learning  
- **Model:** K-Means  
- **Goal:** Group customers based on behavior  

**Features:**
- Annual income  
- Spending score  

Includes:
- Cluster visualization  
- Segment labeling  
- Interactive assignment  

---

### 4. Admission Prediction (Neural Network)
- **Type:** Classification  
- **Model:** MLPClassifier (Neural Network)  
- **Goal:** Classify admission likelihood  

**Features:**
- GRE score  
- TOEFL score  
- CGPA  
- SOP & LOR ratings  
- Research experience  

---

## Architecture

```text
ml-portfolio-dashboard/
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
├── data/
├── models/
├── documentation/
│   ├── report.pdf
│   └── presentation.pdf
└── src/
    ├── clustering/
    ├── loan_eligibility/
    ├── neural_network/
    ├── real_estate/
    └── utils/
```

## Installation

```
git clone https://github.com/KarimGuida/ml-portfolio-dashboard.git
cd ml-portfolio-dashboard
```
```
pip install -r requirements.txt
streamlit run app.py
```