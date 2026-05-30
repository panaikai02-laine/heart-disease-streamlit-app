import streamlit as st
import pandas as pd
import joblib
import os
import html



st.set_page_config(
    page_title="Heart Disease Risk Prediction",
    page_icon="❤️",
    layout="wide"
)


st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 18% 12%, rgba(37, 99, 235, 0.13), transparent 32%),
        radial-gradient(circle at 85% 18%, rgba(20, 184, 166, 0.10), transparent 30%),
        radial-gradient(circle at 50% 95%, rgba(124, 58, 237, 0.09), transparent 34%),
        linear-gradient(135deg, #070a12 0%, #0a0f1a 45%, #05070d 100%) !important;
    background-size: 160% 160%;
    animation: softGlowMove 24s ease-in-out infinite;
    color: #ffffff !important;
}

@keyframes softGlowMove {
    0% {
        background-position: 0% 0%;
    }
    50% {
        background-position: 80% 70%;
    }
    100% {
        background-position: 0% 0%;
    }
}

}
[data-testid="stAppViewContainer"] {
    background: transparent !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #232431 0%, #1b1c27 100%) !important;
}

.block-container {
    background: transparent !important;
}
.hero-card {
    padding: 28px 32px;
    margin-bottom: 26px;
    border-radius: 24px;
    background: linear-gradient(135deg, rgba(255,255,255,0.07), rgba(255,255,255,0.025));
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 20px 50px rgba(0,0,0,0.25);
    backdrop-filter: blur(12px);
    position: relative;
    overflow: hidden;
}

.hero-card::before {
    content: "";
    position: absolute;
    left: 0;
    top: 22px;
    bottom: 22px;
    width: 5px;
    border-radius: 999px;
    background: linear-gradient(180deg, #ef4444, #facc15, #22c55e);
}

.hero-badge {
    display: inline-block;
    padding: 6px 12px;
    margin-bottom: 12px;
    border-radius: 999px;
    background: rgba(239, 68, 68, 0.14);
    color: #fecaca;
    font-size: 13px;
    font-weight: 800;
    border: 1px solid rgba(239, 68, 68, 0.30);
}

.main-title {
    display: flex;
    align-items: center;
    gap: 14px;
    font-size: 44px;
    font-weight: 950;
    color: #ffffff;
    margin-bottom: 10px;
    line-height: 1.15;
    letter-spacing: -0.8px;
}

.medical-heart {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 58px;
    height: 58px;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.24), rgba(127, 29, 29, 0.22));
    border: 1px solid rgba(248, 113, 113, 0.38);
    box-shadow: 0 14px 35px rgba(239, 68, 68, 0.20);
    font-size: 36px;
}

.heart-symbol {
    display: inline-block;
    transform-origin: center;
    animation: elegantHeartPump 1.65s ease-in-out infinite;
    filter: drop-shadow(0 0 8px rgba(239, 68, 68, 0.30));
    will-change: transform, filter;
}

@keyframes elegantHeartPump {
    0%, 100% {
        transform: scale(1);
        filter: drop-shadow(0 0 8px rgba(239, 68, 68, 0.30));
    }

    12% {
        transform: scale(1.06);
        filter: drop-shadow(0 0 11px rgba(239, 68, 68, 0.38));
    }

    22% {
        transform: scale(0.99);
    }

    34% {
        transform: scale(1.12);
        filter: drop-shadow(0 0 14px rgba(239, 68, 68, 0.45));
    }

    48% {
        transform: scale(1);
    }
}
.subtitle {
    font-size: 17px;
    color: #d1d5db;
    line-height: 1.6;
    max-width: 1000px;
}

@media (max-width: 768px) {
    .hero-card {
        padding: 22px 20px;
        border-radius: 20px;
    }

    .main-title {
        font-size: 32px;
        gap: 10px;
    }

    .medical-heart {
        min-width: 48px;
        height: 48px;
        font-size: 30px;
        border-radius: 15px;
    }

    .subtitle {
        font-size: 15px;
    }
}
div[data-testid="stTextInput"],
div[data-testid="stNumberInput"],
div[data-testid="stSelectbox"] {
    padding: 6px;
    border-radius: 12px;
    border: 1px solid transparent;
    transition: all 0.25s ease-in-out;
}
div[data-testid="stTextInput"]:hover,
div[data-testid="stNumberInput"]:hover,
div[data-testid="stSelectbox"]:hover {
    border-color: rgba(88, 166, 255, 0.7);
    box-shadow: 0 0 18px rgba(88, 166, 255, 0.22);
    background: rgba(88, 166, 255, 0.04);
}
div.stButton > button {
    background-color: #238636;
    color: white;
    border-radius: 10px;
    padding: 0.6rem 1.2rem;
    border: none;
    font-weight: 800;
    transition: all 0.25s ease-in-out;
}
div.stButton > button:hover {
    background-color: #2ea043;
    transform: scale(1.03);
    box-shadow: 0 0 16px rgba(46,160,67,0.45);
    color: white;
}
.bmi-box {
    background: #0d1117;
    border: 1px solid #30363d;
    padding: 16px;
    border-radius: 12px;
    margin-top: 10px;
    margin-bottom: 18px;
    box-shadow: 0 0 14px rgba(88,166,255,0.12);
}
.medical-alert-card {
    margin-top: 18px;
    margin-bottom: 22px;
    padding: 22px 26px;
    border-radius: 18px;
    background: linear-gradient(135deg, rgba(255,75,75,0.18), rgba(255,193,7,0.12));
    border: 1.5px solid rgba(255,193,7,0.75);
    box-shadow: 0 0 24px rgba(255,193,7,0.18);
    transition: all 0.25s ease-in-out;
}
.medical-alert-card:hover {
    transform: translateY(-3px);
    border-color: #ffcc00;
    box-shadow: 0 0 32px rgba(255,193,7,0.35);
}
.medical-alert-title {
    font-size: 24px;
    font-weight: 900;
    color: #ffd166;
    margin-bottom: 8px;
}
.medical-alert-text {
    font-size: 16px;
    line-height: 1.7;
    color: #f5f5f5;
}
.result-card {
    background: linear-gradient(135deg, rgba(88,166,255,0.16), rgba(46,160,67,0.10));
    border: 1px solid rgba(88,166,255,0.60);
    border-radius: 18px;
    padding: 24px;
    margin-top: 20px;
    margin-bottom: 22px;
    box-shadow: 0 0 22px rgba(88,166,255,0.14);
    transition: all 0.25s ease-in-out;
}
.result-card:hover {
    transform: translateY(-3px);
    border-color: #58a6ff;
    box-shadow: 0 0 32px rgba(88,166,255,0.28);
}
.result-title {
    font-size: 30px;
    font-weight: 900;
    color: #ffffff;
    margin-bottom: 18px;
}
.result-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
    gap: 16px;
}
.result-box {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 14px;
    padding: 18px;
    text-align: center;
    transition: all 0.25s ease-in-out;
}
.result-box:hover {
    transform: translateY(-3px);
    border-color: #58a6ff;
    box-shadow: 0 0 18px rgba(88,166,255,0.22);
}
.result-label {
    font-size: 13px;
    color: #b0b0b0;
    margin-bottom: 8px;
}
.result-value {
    font-size: 23px;
    font-weight: 900;
    color: #ffffff;
}
.result-low {
    font-size: 25px;
    font-weight: 900;
    color: #2ecc71;
}
.result-medium {
    font-size: 25px;
    font-weight: 900;
    color: #f1c40f;
}
.result-high {
    font-size: 25px;
    font-weight: 900;
    color: #ff4b4b;
}
.result-message {
    margin-top: 18px;
    padding: 14px 16px;
    border-radius: 12px;
    background: rgba(255,255,255,0.04);
    border: 1px solid #30363d;
    color: #e6edf3;
}
.footer-box-final {
    margin-top: 45px;
    padding: 28px;
    border-radius: 16px;
    background: #0d1117;
    border: 1px solid #30363d;
    color: #c9d1d9;
    text-align: center;
    transition: all .25s ease-in-out;
}
.footer-box-final:hover {
    border-color: #58a6ff;
    box-shadow: 0 0 22px rgba(88,166,255,.20);
}
.footer-title-final {
    font-size: 21px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 14px;
}
.group-names-final {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 18px;
    flex-wrap: wrap;
    margin-bottom: 24px;
    font-size: 17px;
    font-weight: 600;
}
.group-name-final {
    background: #161b22;
    padding: 10px 16px;
    border-radius: 12px;
    border: 1px solid #30363d;
    transition: all .25s ease-in-out;
}
.group-name-final:hover {
    transform: translateY(-3px);
    border-color: #58a6ff;
    box-shadow: 0 0 16px rgba(88,166,255,.25);
}
.tools-used-final {
    max-width: 950px;
    margin: auto;
    line-height: 1.8;
}
.small-note-final {
    color: #b0b0b0;
    font-size: 14px;
    margin-top: 18px;
}


</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
.reco-section-title {
    font-size: 32px;
    font-weight: 900;
    color: #ffffff;
    margin-top: 28px;
    margin-bottom: 8px;
}
.reco-section-subtitle {
    color: #b0b0b0;
    font-size: 15px;
    margin-bottom: 18px;
}
.reco-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 18px;
    margin-top: 16px;
    margin-bottom: 24px;
}
.reco-card {
    background: linear-gradient(135deg, rgba(46,160,67,0.13), rgba(88,166,255,0.10));
    border: 1px solid #30363d;
    border-radius: 18px;
    padding: 20px;
    min-height: 185px;
    transition: all 0.25s ease-in-out;
    box-shadow: 0 0 16px rgba(88,166,255,0.08);
}
.reco-card:hover {
    transform: translateY(-5px);
    border-color: #58a6ff;
    box-shadow: 0 0 30px rgba(88,166,255,0.26);
}
.reco-icon {
    width: 58px;
    height: 58px;
    border-radius: 16px;
    background: #0d1117;
    border: 1px solid #30363d;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 31px;
    margin-bottom: 14px;
    box-shadow: 0 0 14px rgba(46,160,67,0.16);
}
.reco-title {
    font-size: 19px;
    font-weight: 900;
    color: #ffffff;
    margin-bottom: 8px;
}
.reco-text {
    font-size: 15px;
    line-height: 1.6;
    color: #d0d0d0;
}
.reco-tag {
    display: inline-block;
    margin-top: 12px;
    padding: 5px 10px;
    border-radius: 999px;
    background: rgba(46,160,67,0.16);
    border: 1px solid rgba(46,160,67,0.35);
    color: #8be28b;
    font-size: 12px;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)



ARTIFACT_FOLDER = "."

best_model = joblib.load(os.path.join(ARTIFACT_FOLDER, "best_model.pkl"))
minmax_scaler = joblib.load(os.path.join(ARTIFACT_FOLDER, "minmax_scaler.pkl"))
top10_features = joblib.load(os.path.join(ARTIFACT_FOLDER, "top10_features.pkl"))
model_metrics = pd.read_csv(os.path.join(ARTIFACT_FOLDER, "model_metrics.csv"))
shap_importance = pd.read_csv(os.path.join(ARTIFACT_FOLDER, "shap_importance.csv"))

bmi_index = top10_features.index("BMI")
bmi_min_value = float(minmax_scaler.data_min_[bmi_index])
bmi_max_value = float(minmax_scaler.data_max_[bmi_index])


def get_risk_level(probability):
    if probability < 0.20:
        return "Low Risk", "🟢", "result-low"
    elif probability < 0.50:
        return "Medium Risk", "🟡", "result-medium"
    else:
        return "High Risk", "🔴", "result-high"


def generate_lifestyle_recommendations(user_data):
    recommendations = []

    if user_data["HighBP"] == 1:
        recommendations.append("Monitor blood pressure regularly and reduce high-sodium foods.")

    if user_data["HighChol"] == 1:
        recommendations.append("Limit fatty and high-cholesterol foods and consult a healthcare professional.")

    if user_data["BMI"] >= 30:
        recommendations.append("Maintain a healthier weight through balanced diet and regular physical activity.")

    if user_data["Smoker"] == 1:
        recommendations.append("Consider quitting smoking to reduce heart disease risk.")

    if user_data["Diabetes"] > 0:
        recommendations.append("Monitor blood sugar levels and follow proper diabetes care.")

    if user_data["PhysActivity"] == 0:
        recommendations.append("Increase physical activity such as walking, stretching, or light exercise.")

    if user_data["GenHlth"] >= 4:
        recommendations.append("Schedule regular health check-ups to monitor overall health.")

    if user_data["Stroke"] == 1:
        recommendations.append("Continue medical follow-up because stroke history may increase heart-related risk.")

    if len(recommendations) == 0:
        recommendations.append("Maintain a healthy lifestyle, balanced diet, regular activity, and routine check-ups.")

    return recommendations



def generate_recommendation_cards(user_data):
    cards = []

    if user_data["HighBP"] == 1:
        cards.append({
            "icon": "🩺",
            "title": "Monitor Blood Pressure",
            "text": "Check blood pressure regularly and reduce high-sodium foods such as salty snacks, processed food, and instant meals.",
            "tag": "Blood Pressure"
        })

    if user_data["HighChol"] == 1:
        cards.append({
            "icon": "🥗",
            "title": "Support Healthy Cholesterol",
            "text": "Limit fatty and high-cholesterol foods. Choose more vegetables, fruits, whole grains, and consult a healthcare professional.",
            "tag": "Cholesterol"
        })

    if user_data["BMI"] >= 30:
        cards.append({
            "icon": "⚖️",
            "title": "Manage Healthy Weight",
            "text": "Maintain a healthier weight through balanced meals, proper portions, enough sleep, and regular physical activity.",
            "tag": "BMI / Weight"
        })

    if user_data["Smoker"] == 1:
        cards.append({
            "icon": "🚭",
            "title": "Reduce Smoking Risk",
            "text": "Consider quitting smoking or seeking support to reduce heart-related risk and improve overall cardiovascular health.",
            "tag": "Smoking"
        })

    if user_data["Diabetes"] > 0:
        cards.append({
            "icon": "🩸",
            "title": "Monitor Blood Sugar",
            "text": "Monitor blood sugar levels, follow proper diabetes care, and consult a healthcare provider for safe management.",
            "tag": "Diabetes"
        })

    if user_data["PhysActivity"] == 0:
        cards.append({
            "icon": "🚶",
            "title": "Increase Physical Activity",
            "text": "Try light activities such as walking, stretching, or simple home exercises, based on what is safe for your condition.",
            "tag": "Exercise"
        })

    if user_data["GenHlth"] >= 4:
        cards.append({
            "icon": "📅",
            "title": "Schedule Health Check-ups",
            "text": "Regular check-ups can help monitor symptoms, detect risks earlier, and guide proper lifestyle or medical action.",
            "tag": "Check-up"
        })

    if user_data["Stroke"] == 1:
        cards.append({
            "icon": "🧠",
            "title": "Continue Medical Follow-up",
            "text": "A history of stroke may increase heart-related risk, so continuous monitoring and medical follow-up are important.",
            "tag": "Stroke History"
        })

    if len(cards) == 0:
        cards.append({
            "icon": "💚",
            "title": "Maintain Healthy Habits",
            "text": "Continue a balanced diet, regular physical activity, enough rest, stress management, and routine health check-ups.",
            "tag": "General Wellness"
        })

    return cards


def get_shap_based_factors(user_data, shap_importance):
    factors = []

    for _, row in shap_importance.iterrows():
        feature = row["Feature"]

        if feature == "Age" and user_data["Age"] >= 8:
            factors.append("Older age category was identified as a risk-related factor in this prediction.")
        elif feature == "GenHlth" and user_data["GenHlth"] >= 4:
            factors.append("Fair or poor general health was identified as a risk-related factor in this prediction.")
        elif feature == "Sex" and user_data["Sex"] == 1:
            factors.append("Sex-related pattern was identified as a model-related factor in this prediction.")
        elif feature == "HighChol" and user_data["HighChol"] == 1:
            factors.append("High cholesterol was identified as a risk-related factor in this prediction.")
        elif feature == "HighBP" and user_data["HighBP"] == 1:
            factors.append("High blood pressure was identified as a risk-related factor in this prediction.")
        elif feature == "Smoker" and user_data["Smoker"] == 1:
            factors.append("Smoking history was identified as a risk-related factor in this prediction.")
        elif feature == "Diabetes" and user_data["Diabetes"] > 0:
            factors.append("Diabetes or prediabetes was identified as a risk-related factor in this prediction.")
        elif feature == "Stroke" and user_data["Stroke"] == 1:
            factors.append("History of stroke was identified as a risk-related factor in this prediction.")
        elif feature == "BMI" and user_data["BMI"] >= 30:
            factors.append("High BMI was identified as a risk-related factor in this prediction.")
        elif feature == "PhysActivity" and user_data["PhysActivity"] == 0:
            factors.append("Lack of physical activity was identified as a risk-related factor in this prediction.")

    if len(factors) == 0:
        factors.append("No major high-risk factor was detected from the selected inputs.")

    return factors[:5]


def show_footer():
    st.markdown(
        '<div class="footer-box-final"><div class="footer-title-final">Developed By</div>'
        '<div class="group-names-final">'
        '<span class="group-name-final">黃漢斯</span>'
        '<span class="group-name-final">吳文娜</span>'
        '<span class="group-name-final">朱諾妃</span>'
        '<span class="group-name-final">程巧雯</span>'
        '<span class="group-name-final">潘艾凱</span>'
        '</div>'
        '<div class="footer-title-final">Used for Development</div>'
        '<div class="tools-used-final">Python • Streamlit • pandas • NumPy • scikit-learn • joblib • Google Colab • GitHub • Streamlit Community Cloud • SHAP-based Explainability</div>'
        '<p class="small-note-final">This web application is for educational and capstone purposes only.</p>'
        '</div>',
        unsafe_allow_html=True
    )


st.markdown("""
<div class="hero-card">
    <div class="hero-badge">AI-Powered Health Risk Screening</div>
    <div class="main-title">
        <span class="medical-heart"><span class="heart-symbol">🫀</span></span>
        <span>Heart Disease Risk Prediction with Explainable AI</span>
    </div>
    <div class="subtitle">
        Predicts HeartDiseaseorAttack risk using the Top 10 selected features, trained model, explanation details, and lifestyle recommendations.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.disclaimer-ticker {
width: 100%;
height: 52px;
overflow: hidden;
white-space: nowrap;
display: flex;
align-items: center;
margin: 18px 0 26px 0;
border-radius: 10px;
background: linear-gradient(90deg, rgba(63, 74, 31, 0.95), rgba(42, 56, 24, 0.95));
border: 1.5px solid rgba(255, 255, 255, 0.70);
box-shadow: 0 0 18px rgba(255, 255, 255, 0.08), 0 10px 28px rgba(0, 0, 0, 0.22);
}

.disclaimer-track {
display: inline-flex;
width: max-content;
animation: tickerMove 28s linear infinite;
}

.disclaimer-text {
display: inline-block;
padding-right: 80px;
color: #fff7cc;
font-weight: 800;
font-size: 15px;
}

@keyframes tickerMove {
0% {
transform: translateX(0);
}
100% {
transform: translateX(-50%);
}
}

@media (max-width: 768px) {
.disclaimer-ticker {
height: 48px;
}

.disclaimer-text {
font-size: 13px;
padding-right: 60px;
}

.disclaimer-track {
animation-duration: 34s;
}
}
</style>
<div class="disclaimer-ticker">
<div class="disclaimer-track">
<span class="disclaimer-text">Disclaimer: This system is for educational and capstone purposes only. It should not replace medical advice from healthcare professionals.</span>
<span class="disclaimer-text">Disclaimer: This system is for educational and capstone purposes only. It should not replace medical advice from healthcare professionals.</span>
<span class="disclaimer-text">Disclaimer: This system is for educational and capstone purposes only. It should not replace medical advice from healthcare professionals.</span>
<span class="disclaimer-text">Disclaimer: This system is for educational and capstone purposes only. It should not replace medical advice from healthcare professionals.</span>
</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
.notice-card {
    display: flex;
    gap: 16px;
    align-items: flex-start;
    padding: 24px 26px;
    border-radius: 20px;
    margin: 22px 0;
    background: rgba(255, 255, 255, 0.055);
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 0 18px 45px rgba(0, 0, 0, 0.22);
    backdrop-filter: blur(10px);
}

.notice-icon {
    width: 46px;
    height: 46px;
    min-width: 46px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 23px;
    background: rgba(255, 255, 255, 0.08);
}

.notice-content h3 {
    margin: 0 0 10px 0;
    font-size: 24px;
    font-weight: 900;
    color: #ffffff;
}

.notice-content p {
    margin: 0 0 12px 0;
    color: #e5e7eb;
    font-size: 15px;
    line-height: 1.65;
}

.warning-card {
    border-left: 5px solid #facc15;
}

.info-card {
    border-left: 5px solid #38bdf8;
}

@media (max-width: 768px) {
    .notice-card {
        padding: 18px;
        gap: 12px;
    }

    .notice-content h3 {
        font-size: 20px;
    }

    .notice-content p {
        font-size: 14px;
    }
}
</style>

<div class="notice-card warning-card">
    <div class="notice-icon">⚠️</div>
    <div class="notice-content">
        <h3>Important Medical Reminder</h3>
        <p>This system provides an <b>AI-based risk estimate only</b>. It is not a medical diagnosis and should not be used as a replacement for professional healthcare advice.</p>
        <p>For accurate evaluation, proper diagnosis, and treatment, it is still best to <b>consult a licensed doctor or healthcare professional</b>.</p>
    </div>
</div>

<div style="display:flex; align-items:center; gap:12px; margin:14px 0 24px 0; padding:14px 18px; border-radius:14px; background:rgba(59,130,246,0.08); border:1px solid rgba(147,197,253,0.22); color:#cbd5e1; font-size:14px; line-height:1.6; box-shadow:0 10px 28px rgba(0,0,0,0.16);">
<div style="display:flex; align-items:center; justify-content:center; min-width:34px; height:34px; border-radius:10px; background:rgba(59,130,246,0.15); font-size:17px;">🔎</div>
<div><b>Screening Note:</b> The risk score is a machine learning probability estimate, not a medical diagnosis. The risk level is interpreted using app-defined thresholds.</div>
</div>

<div class="notice-card info-card">
    <div class="notice-icon">ℹ️</div>
    <div class="notice-content">
        <h3>Risk Factor Interpretation</h3>
        <p>Having one or more risk factors does <b>not automatically mean</b> that a person has heart disease or had a heart attack. The system estimates risk based on patterns learned from the dataset, where some respondents had risk factors but did not report coronary heart disease or myocardial infarction.</p>
    </div>
</div>
""", unsafe_allow_html=True)


st.sidebar.header("System Information")
st.sidebar.write("**Model:** Best selected model from training")
st.sidebar.write("**Best Model:** Logistic Regression")
st.sidebar.write("**Input Features:** Top 10 selected features")
st.sidebar.write("**Explanation:** SHAP-based feature importance")

with st.sidebar.expander("Top 10 Features Used"):
    for feature in top10_features:
        st.write("•", feature)

with st.sidebar.expander("Age Mapping Guide"):
    st.write("1 = 18–24")
    st.write("2 = 25–29")
    st.write("3 = 30–34")
    st.write("4 = 35–39")
    st.write("5 = 40–44")
    st.write("6 = 45–49")
    st.write("7 = 50–54")
    st.write("8 = 55–59")
    st.write("9 = 60–64")
    st.write("10 = 65–69")
    st.write("11 = 70–74")
    st.write("12 = 75–79")
    st.write("13 = 80 or older")

with st.sidebar.expander("Model Evaluation Metrics"):
    metrics_display = model_metrics[[
        "Model", "Accuracy", "Recall", "F1-score", "ROC-AUC"
    ]].copy()

    for col in ["Accuracy", "Recall", "F1-score", "ROC-AUC"]:
        metrics_display[col] = (metrics_display[col] * 100).round(2).astype(str) + "%"

    st.markdown("**Best Model:** Logistic Regression")
    st.markdown("**Model Comparison:**")

    for _, row in metrics_display.iterrows():
        st.markdown(
            f"""
            <div style="
                padding: 10px 12px;
                margin-bottom: 10px;
                border: 1px solid rgba(255,255,255,0.15);
                border-radius: 10px;
                background: rgba(255,255,255,0.04);
                line-height: 1.7;
            ">
                <b>{row['Model']}</b><br>
                Accuracy: {row['Accuracy']}<br>
                Recall: {row['Recall']}<br>
                F1-score: {row['F1-score']}<br>
                ROC-AUC: {row['ROC-AUC']}
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("""
<style>
@media (min-width: 1201px) {
    .block-container {
        padding-right: 360px !important;
    }
}

.right-tips-panel {
    position: fixed;
    right: 22px;
    top: 125px;
    width: 300px;
    z-index: 999;
    background: linear-gradient(145deg, rgba(16, 24, 39, 0.96), rgba(10, 15, 25, 0.96));
    border: 1px solid rgba(59, 130, 246, 0.35);
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 18px 45px rgba(0, 0, 0, 0.35);
}

.right-tips-title {
    font-size: 20px;
    font-weight: 900;
    color: #ffffff;
    margin-bottom: 6px;
}

.right-tips-subtitle {
    font-size: 12px;
    color: #b8c4d8;
    margin-bottom: 14px;
    line-height: 1.5;
}

.health-tip-card {
    background: rgba(255, 255, 255, 0.055);
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 14px;
    padding: 12px;
    margin-bottom: 10px;
    transition: all 0.25s ease;
}

.health-tip-card:hover {
    transform: translateY(-3px);
    border-color: rgba(34, 197, 94, 0.55);
    box-shadow: 0 10px 25px rgba(34, 197, 94, 0.15);
}

.health-tip-card h4 {
    color: #ffffff;
    font-size: 14px;
    margin: 0 0 5px 0;
    font-weight: 800;
}

.health-tip-card p {
    color: #cbd5e1;
    font-size: 12px;
    margin: 0;
    line-height: 1.45;
}

.tip-badge {
    display: inline-block;
    margin-top: 8px;
    padding: 4px 9px;
    border-radius: 999px;
    background: rgba(34, 197, 94, 0.18);
    color: #86efac;
    font-size: 11px;
    font-weight: 700;
}

@media (max-width: 1200px) {
    .block-container {
        padding-right: 1rem !important;
    }

    .right-tips-panel {
        position: static;
        width: auto;
        max-width: 100%;
        margin: 18px 0 26px 0;
        right: auto;
        top: auto;
        z-index: auto;
        padding: 16px;
        border-radius: 16px;
    }
}
</style>

<div class="right-tips-panel">
<div class="right-tips-title">📰 Health Tips</div>
<div class="right-tips-subtitle">General wellness reminders for heart health awareness.</div>

<div class="health-tip-card">
<h4>🩺 Monitor Your Health</h4>
<p>Regular check-ups can help detect possible health risks early.</p>
<span class="tip-badge">Check-up</span>
</div>

<div class="health-tip-card">
<h4>🚶 Stay Physically Active</h4>
<p>Light exercise such as walking may support better cardiovascular health.</p>
<span class="tip-badge">Activity</span>
</div>

<div class="health-tip-card">
<h4>🥗 Choose Balanced Meals</h4>
<p>Limit fatty, salty, and highly processed foods when possible.</p>
<span class="tip-badge">Lifestyle</span>
</div>

<div class="health-tip-card">
<h4>👨‍⚕️ Consult a Doctor</h4>
<p>This system is only a screening support tool and not a medical diagnosis.</p>
<span class="tip-badge">Reminder</span>
</div>
<div class="health-tip-card">
<h4>📊 Understand Risk Levels</h4>
<p>Low, medium, and high risk results are based on the model’s probability threshold.</p>
<span class="tip-badge">Risk Guide</span>
</div>

<div class="health-tip-card">
<h4>💡 Maintain Healthy Habits</h4>
<p>Balanced meals, physical activity, proper rest, and routine check-ups can support heart health.</p>
<span class="tip-badge">Wellness</span>
</div>
</div>
""", unsafe_allow_html=True)

st.header("📝 Health Questionnaire")
st.write(
    "Please complete all required fields. The system will calculate your BMI from your height and weight, "
    "then estimate your heart disease or heart attack risk."
)

name = st.text_input("Full Name", placeholder="Enter your name")

col1, col2 = st.columns(2)

with col1:
    high_bp = st.selectbox(
        "Have you ever been told by a doctor that you have high blood pressure?",
        ["No", "Yes"],
        index=None,
        placeholder="Select an answer"
    )

    height_cm = st.number_input(
        "What is your height? (cm)",
        min_value=80.0,
        max_value=250.0,
        value=None,
        step=0.1,
        placeholder="Enter height in centimeters"
    )

    weight_kg = st.number_input(
        "What is your weight? (kg)",
        min_value=20.0,
        max_value=300.0,
        value=None,
        step=0.1,
        placeholder="Enter weight in kilograms"
    )

    calculated_bmi = None
    if height_cm is not None and weight_kg is not None and height_cm > 0:
        height_m = height_cm / 100
        calculated_bmi = weight_kg / (height_m ** 2)

        st.markdown(
            f'<div class="bmi-box"><b>Calculated BMI:</b> {calculated_bmi:.2f}<br>'
            f'<span class="small-note-final">BMI training range accepted by the model: {bmi_min_value:.0f} to {bmi_max_value:.0f}</span></div>',
            unsafe_allow_html=True
        )

    age = st.selectbox(
        "What is your age group?",
        [
            "18–24", "25–29", "30–34", "35–39", "40–44",
            "45–49", "50–54", "55–59", "60–64", "65–69",
            "70–74", "75–79", "80 or older"
        ],
        index=None,
        placeholder="Select age category"
    )

    smoker = st.selectbox(
        "Have you smoked at least 100 cigarettes in your lifetime?",
        ["No", "Yes"],
        index=None,
        placeholder="Select an answer"
    )

with col2:
    diabetes = st.selectbox(
        "Have you ever been told that you have diabetes?",
        ["No Diabetes", "Prediabetes", "Diabetes"],
        index=None,
        placeholder="Select diabetes status"
    )

    phys_activity = st.selectbox(
        "Have you done any physical activity or exercise in the past 30 days?",
        ["No", "Yes"],
        index=None,
        placeholder="Select an answer"
    )

    high_chol = st.selectbox(
        "Have you ever been told by a doctor that you have high cholesterol?",
        ["No", "Yes"],
        index=None,
        placeholder="Select an answer"
    )

    gen_hlth = st.selectbox(
        "How would you describe your overall health?",
        ["Excellent", "Very Good", "Good", "Fair", "Poor"],
        index=None,
        placeholder="Select general health"
    )

    stroke = st.selectbox(
        "Have you ever been told that you had a stroke?",
        ["No", "Yes"],
        index=None,
        placeholder="Select an answer"
    )

    sex = st.selectbox(
        "Sex",
        ["Female", "Male"],
        index=None,
        placeholder="Select sex"
    )

submitted = st.button("Check Result")


if submitted:
    required_fields = {
        "Full Name": name.strip(),
        "High Blood Pressure": high_bp,
        "Height": height_cm,
        "Weight": weight_kg,
        "Age Group": age,
        "Smoking History": smoker,
        "Diabetes Status": diabetes,
        "Physical Activity": phys_activity,
        "High Cholesterol": high_chol,
        "General Health": gen_hlth,
        "Stroke History": stroke,
        "Sex": sex
    }

    missing_fields = [
        field for field, value in required_fields.items()
        if value is None or value == ""
    ]

    if missing_fields:
        st.error(
            "Important: Please fill in all required fields before checking the result. "
            "Missing field(s): " + ", ".join(missing_fields)
        )
        show_footer()
        st.stop()

    if calculated_bmi is None:
        st.error("Please enter valid height and weight values.")
        show_footer()
        st.stop()

    if calculated_bmi < bmi_min_value or calculated_bmi > bmi_max_value:
        st.error(
            f"Calculated BMI is {calculated_bmi:.2f}, which is outside the model's training BMI range "
            f"({bmi_min_value:.0f} to {bmi_max_value:.0f}). Please check the height and weight values."
        )
        show_footer()
        st.stop()

    age_mapping = {
        "18–24": 1,
        "25–29": 2,
        "30–34": 3,
        "35–39": 4,
        "40–44": 5,
        "45–49": 6,
        "50–54": 7,
        "55–59": 8,
        "60–64": 9,
        "65–69": 10,
        "70–74": 11,
        "75–79": 12,
        "80 or older": 13
    }

    diabetes_mapping = {
        "No Diabetes": 0,
        "Prediabetes": 1,
        "Diabetes": 2
    }

    gen_health_mapping = {
        "Excellent": 1,
        "Very Good": 2,
        "Good": 3,
        "Fair": 4,
        "Poor": 5
    }

    user_data = {
        "HighBP": 1 if high_bp == "Yes" else 0,
        "BMI": calculated_bmi,
        "Age": age_mapping[age],
        "Smoker": 1 if smoker == "Yes" else 0,
        "Diabetes": diabetes_mapping[diabetes],
        "PhysActivity": 1 if phys_activity == "Yes" else 0,
        "HighChol": 1 if high_chol == "Yes" else 0,
        "GenHlth": gen_health_mapping[gen_hlth],
        "Stroke": 1 if stroke == "Yes" else 0,
        "Sex": 1 if sex == "Male" else 0
    }

    input_df = pd.DataFrame([user_data])
    input_df = input_df[top10_features]

    input_scaled_array = minmax_scaler.transform(input_df)
    input_scaled = pd.DataFrame(input_scaled_array, columns=top10_features)
    risk_probability = best_model.predict_proba(input_scaled)[0][1]
    risk_score = risk_probability * 100

    risk_level, risk_icon, risk_css_class = get_risk_level(risk_probability)
    safe_name = html.escape(name.strip())

    result_html = (
        f'<div class="result-card">'
        f'<div class="result-title">📊 Risk Prediction Result</div>'
        f'<div class="result-grid">'
        f'<div class="result-box"><div class="result-label">Patient / User Name</div><div class="result-value">{safe_name}</div></div>'
        f'<div class="result-box"><div class="result-label">Calculated BMI</div><div class="result-value">{calculated_bmi:.2f}</div></div>'
        f'<div class="result-box"><div class="result-label">Risk Score</div><div class="result-value">{risk_score:.2f}%</div></div>'
        f'<div class="result-box"><div class="result-label">Risk Level</div><div class="{risk_css_class}">{risk_icon} {risk_level}</div></div>'
        f'<div class="result-box"><div class="result-label">Prediction Model</div><div class="result-value">Logistic Regression</div></div>'
        f'</div>'
        f'<div class="result-message">The result is an AI-based probability estimate and should be interpreted as a screening support only.</div>'
        f'</div>'
    )

    st.markdown(result_html, unsafe_allow_html=True)

    if risk_level == "Low Risk":
        st.success("The predicted result shows a low risk level.")
    elif risk_level == "Medium Risk":
        st.warning("The predicted result shows a medium risk level.")
    else:
        st.error("The predicted result shows a high risk level.")

    with st.expander("View Explanation Details", expanded=False):
        st.write(
            "This section provides an explanation based on the saved SHAP importance results "
            "from the trained model and the user's current input values."
        )

        top_factors = get_shap_based_factors(user_data, shap_importance)

        st.subheader("Top Contributing Factors")
        for factor in top_factors:
            st.write("•", factor)

        st.subheader("Global SHAP Feature Importance")
        st.text(shap_importance.to_string(index=False))

    st.markdown('<div class="reco-section-title">💡 Personalized Lifestyle Recommendations</div>', unsafe_allow_html=True)
    st.markdown('<div class="reco-section-subtitle">Suggested lifestyle actions based on the user\'s current input values. These are general wellness suggestions and not medical prescriptions.</div>', unsafe_allow_html=True)

    recommendation_cards = generate_recommendation_cards(user_data)

    reco_html = '<div class="reco-grid">'
    for card in recommendation_cards:
        reco_html += (
            f'<div class="reco-card">'
            f'<div class="reco-icon">{card["icon"]}</div>'
            f'<div class="reco-title">{card["title"]}</div>'
            f'<div class="reco-text">{card["text"]}</div>'
            f'<div class="reco-tag">{card["tag"]}</div>'
            f'</div>'
        )
    reco_html += '</div>'

    st.markdown(reco_html, unsafe_allow_html=True)

    with st.expander("View Encoded Input Used by the Model"):
        encoded_display = pd.DataFrame({
            "Feature": input_df.columns,
            "Encoded Value": input_df.iloc[0].values
        })
        st.table(encoded_display)

else:
    st.info("Complete the health questionnaire and click Check Result to view your calculated BMI, risk score, explanation, and recommendations.")

show_footer()
