import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# --- SIMPLE PREDICT FUNCTION (to replace prediction_helper.py) ---
def predict(age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
            delinquency_ratio, credit_utilization_ratio, num_open_accounts,
            residence_type, loan_purpose, loan_type):
    """Simple credit score calculator - NO EXTERNAL DEPENDENCIES"""
    
    # Base score calculation
    base_score = 650
    
    # Age factor
    if 25 <= age <= 35:
        base_score += 30
    elif 36 <= age <= 50:
        base_score += 40
    else:
        base_score += 20
    
    # Income factor
    if income > 2000000:
        base_score += 50
    elif income > 1000000:
        base_score += 30
    elif income > 500000:
        base_score += 15
    
    # Loan-to-income penalty
    lti_ratio = (loan_amount / income * 100) if income > 0 else 0
    if lti_ratio > 50:
        base_score -= 40
    elif lti_ratio > 30:
        base_score -= 20
    
    # Credit utilization penalty
    if credit_utilization_ratio > 70:
        base_score -= 40
    elif credit_utilization_ratio > 50:
        base_score -= 20
    elif credit_utilization_ratio < 30:
        base_score += 15
    
    # Delinquency penalty
    if delinquency_ratio > 30:
        base_score -= 40
    elif delinquency_ratio > 15:
        base_score -= 20
    
    # DPD penalty
    if avg_dpd_per_delinquency > 60:
        base_score -= 30
    elif avg_dpd_per_delinquency > 30:
        base_score -= 15
    
    # Residence bonus
    if residence_type == "Owned":
        base_score += 25
    elif residence_type == "Mortgage":
        base_score += 10
    
    # Loan purpose adjustment
    if loan_purpose == "Home":
        base_score += 20
    elif loan_purpose == "Education":
        base_score += 15
    
    # Ensure score is within range
    credit_score = max(300, min(int(base_score), 850))
    
    # Calculate default probability
    default_probability = max(0.01, min(0.99, (850 - credit_score) / 550 * 0.8))
    
    # Determine rating
    if credit_score >= 750:
        rating = "Excellent"
    elif credit_score >= 650:
        rating = "Good"
    elif credit_score >= 550:
        rating = "Fair"
    else:
        rating = "Poor"
    
    return default_probability, credit_score, rating

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="EliteCredit Advisor Portal",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- VIBRANT JEWEL-TONE FINANCIAL CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700;800&display=swap');

    /* === VIBRANT MESH GRADIENT BACKGROUND === */
    .stApp {
        background: linear-gradient(135deg, 
            #EEF2FF 0%, 
            #E0E7FF 25%, 
            #FDF2F8 50%, 
            #F0F9FF 75%, 
            #F0FDF4 100%) !important;
        background-attachment: fixed !important;
        min-height: 100vh;
    }

    /* === TYPOGRAPHY - DEEP NAVY FOR MAXIMUM READABILITY === */
    html, body, [class*="css"], .stMarkdown, p, div, span, label {
        color: #1E1B4B !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-weight: 400 !important;
    }

    h1, h2, h3, h4, h5, h6, .section-title {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        color: #1E1B4B !important;
        letter-spacing: -0.02em !important;
    }

    /* === PREMIUM GLASSMORPHISM CONTAINER === */
    .premium-container {
        background: rgba(255, 255, 255, 0.75) !important;
        backdrop-filter: blur(24px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
        border-radius: 32px !important;
        padding: 48px !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 
            0 40px 80px -20px rgba(67, 56, 202, 0.15),
            0 20px 40px -20px rgba(99, 102, 241, 0.1),
            inset 0 1px 0 0 rgba(255, 255, 255, 0.2) !important;
        margin: 40px auto !important;
        max-width: 1400px !important;
        position: relative !important;
        overflow: hidden !important;
    }

    /* VIBRANT ACCENT BORDER - ROYAL BLUE */
    .premium-container::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 6px !important;
        background: linear-gradient(90deg, #4338CA, #6366F1, #06B6D4) !important;
        border-radius: 32px 32px 0 0 !important;
    }

    /* === COLOR-CODED FORM CARDS === */
    .form-card {
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(12px) !important;
        padding: 32px !important;
        border-radius: 24px !important;
        margin-bottom: 28px !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }

    /* PERSONAL INFO CARD - BLUE THEME */
    .form-card.personal {
        border: 2px solid rgba(67, 56, 202, 0.3) !important;
        box-shadow: 0 12px 32px -8px rgba(67, 56, 202, 0.08) !important;
    }

    .form-card.personal:hover {
        border-color: rgba(67, 56, 202, 0.5) !important;
        box-shadow: 0 20px 50px -12px rgba(67, 56, 202, 0.15) !important;
        transform: translateY(-4px) !important;
    }

    /* FINANCIAL CAPACITY CARD - PURPLE THEME */
    .form-card.financial {
        border: 2px solid rgba(139, 92, 246, 0.3) !important;
        box-shadow: 0 12px 32px -8px rgba(139, 92, 246, 0.08) !important;
    }

    .form-card.financial:hover {
        border-color: rgba(139, 92, 246, 0.5) !important;
        box-shadow: 0 20px 50px -12px rgba(139, 92, 246, 0.15) !important;
        transform: translateY(-4px) !important;
    }

    /* CREDIT HISTORY CARD - EMERALD THEME */
    .form-card.credit {
        border: 2px solid rgba(16, 185, 129, 0.3) !important;
        box-shadow: 0 12px 32px -8px rgba(16, 185, 129, 0.08) !important;
    }

    .form-card.credit:hover {
        border-color: rgba(16, 185, 129, 0.5) !important;
        box-shadow: 0 20px 50px -12px rgba(16, 185, 129, 0.15) !important;
        transform: translateY(-4px) !important;
    }

    /* FORM HEADERS WITH COLOR-CODED ACCENTS */
    .form-header {
        color: #1E1B4B !important;
        font-weight: 700 !important;
        font-size: 1.3rem !important;
        margin-bottom: 28px !important;
        font-family: 'Outfit', sans-serif !important;
        display: flex !important;
        align-items: center !important;
        gap: 16px !important;
        padding-bottom: 16px !important;
        border-bottom: 2px solid !important;
    }

    .form-header.personal { border-bottom-color: rgba(67, 56, 202, 0.2) !important; }
    .form-header.financial { border-bottom-color: rgba(139, 92, 246, 0.2) !important; }
    .form-header.credit { border-bottom-color: rgba(16, 185, 129, 0.2) !important; }

    /* === VIBRANT INPUT FIELDS === */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div {
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(8px) !important;
        border: 2px solid rgba(203, 213, 225, 0.5) !important;
        color: #1E1B4B !important;
        border-radius: 14px !important;
        height: 58px !important;
        padding: 18px 20px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        min-height: 58px !important;
        transition: all 0.3s ease !important;
    }

    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus {
        border-color: #4338CA !important;
        box-shadow: 0 0 0 4px rgba(67, 56, 202, 0.1) !important;
        outline: none !important;
        background: rgba(255, 255, 255, 0.95) !important;
        transform: translateY(-2px) !important;
    }

    .stSlider > div > div > div > div {
        padding: 24px 0 !important;
    }

    /* === COLORFUL METRIC CARDS WITH UNIQUE IDENTITIES === */
    .metric-card {
        background: rgba(255, 255, 255, 0.85) !important;
        backdrop-filter: blur(12px) !important;
        padding: 28px !important;
        border-radius: 20px !important;
        text-align: center !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }

    .metric-card::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 4px !important;
    }

    /* LTI METRIC - INDIGO THEME */
    .metric-card.lti {
        border: 2px solid rgba(79, 70, 229, 0.3) !important;
        box-shadow: 0 12px 32px -8px rgba(79, 70, 229, 0.1) !important;
    }

    .metric-card.lti::before {
        background: linear-gradient(90deg, #4338CA, #6366F1) !important;
    }

    .metric-card.lti:hover {
        border-color: rgba(79, 70, 229, 0.5) !important;
        box-shadow: 0 20px 50px -12px rgba(79, 70, 229, 0.2) !important;
        transform: translateY(-6px) !important;
    }

    /* DTI METRIC - VIOLET THEME */
    .metric-card.dti {
        border: 2px solid rgba(139, 92, 246, 0.3) !important;
        box-shadow: 0 12px 32px -8px rgba(139, 92, 246, 0.1) !important;
    }

    .metric-card.dti::before {
        background: linear-gradient(90deg, #7C3AED, #8B5CF6) !important;
    }

    .metric-card.dti:hover {
        border-color: rgba(139, 92, 246, 0.5) !important;
        box-shadow: 0 20px 50px -12px rgba(139, 92, 246, 0.2) !important;
        transform: translateY(-6px) !important;
    }

    /* EMI METRIC - TEAL THEME */
    .metric-card.emi {
        border: 2px solid rgba(6, 182, 212, 0.3) !important;
        box-shadow: 0 12px 32px -8px rgba(6, 182, 212, 0.1) !important;
    }

    .metric-card.emi::before {
        background: linear-gradient(90deg, #0891B2, #06B6D4) !important;
    }

    .metric-card.emi:hover {
        border-color: rgba(6, 182, 212, 0.5) !important;
        box-shadow: 0 20px 50px -12px rgba(6, 182, 212, 0.2) !important;
        transform: translateY(-6px) !important;
    }

    .metric-value {
        font-family: 'Outfit', sans-serif !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        margin: 16px 0 8px !important;
        letter-spacing: -0.02em !important;
        background: linear-gradient(135deg, #1E1B4B, #4338CA) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }

    .metric-label {
        font-size: 0.9rem !important;
        color: #4B5563 !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
    }

    .metric-subtitle {
        font-size: 0.85rem !important;
        color: #6B7280 !important;
        margin-top: 6px !important;
        font-weight: 500 !important;
    }

    /* === ANIMATED SCORE SPOTLIGHT === */
    .score-spotlight {
        text-align: center !important;
        padding: 40px 0 !important;
        position: relative !important;
    }

    .score-circle {
        width: 220px !important;
        height: 220px !important;
        border-radius: 50% !important;
        margin: 0 auto 32px !important;
        background: rgba(255, 255, 255, 0.9) !important;
        backdrop-filter: blur(12px) !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        border: 16px solid !important;
        box-shadow: 0 20px 60px -20px rgba(0, 0, 0, 0.15) !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }

    @keyframes pulse-sapphire {
        0% { box-shadow: 0 20px 60px -20px rgba(0, 0, 0, 0.15), 0 0 0 0px rgba(67, 56, 202, 0.4); }
        70% { box-shadow: 0 20px 60px -20px rgba(0, 0, 0, 0.15), 0 0 0 25px rgba(67, 56, 202, 0); }
        100% { box-shadow: 0 20px 60px -20px rgba(0, 0, 0, 0.15), 0 0 0 0px rgba(67, 56, 202, 0); }
    }

    @keyframes pulse-emerald {
        0% { box-shadow: 0 20px 60px -20px rgba(0, 0, 0, 0.15), 0 0 0 0px rgba(16, 185, 129, 0.4); }
        70% { box-shadow: 0 20px 60px -20px rgba(0, 0, 0, 0.15), 0 0 0 25px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 20px 60px -20px rgba(0, 0, 0, 0.15), 0 0 0 0px rgba(16, 185, 129, 0); }
    }

    @keyframes pulse-ruby {
        0% { box-shadow: 0 20px 60px -20px rgba(0, 0, 0, 0.15), 0 0 0 0px rgba(239, 68, 68, 0.4); }
        70% { box-shadow: 0 20px 60px -20px rgba(0, 0, 0, 0.15), 0 0 0 25px rgba(239, 68, 68, 0); }
        100% { box-shadow: 0 20px 60px -20px rgba(0, 0, 0, 0.15), 0 0 0 0px rgba(239, 68, 68, 0); }
    }

    .score-excellent { 
        border-color: #4338CA !important; 
        animation: pulse-sapphire 3s infinite !important;
    }

    .score-good { 
        border-color: #10B981 !important; 
        animation: pulse-emerald 3s infinite !important;
    }

    .score-poor { 
        border-color: #EF4444 !important; 
        animation: pulse-ruby 3s infinite !important;
    }

    .score-circle:hover {
        transform: scale(1.08) rotate(5deg) !important;
        box-shadow: 0 30px 80px -25px rgba(0, 0, 0, 0.2) !important;
    }

    /* === CLIENT BANNER === */
    .client-banner {
        background: linear-gradient(90deg, 
            rgba(255, 255, 255, 0.85) 0%, 
            rgba(255, 255, 255, 0.7) 100%) !important;
        backdrop-filter: blur(16px) !important;
        border: 2px solid rgba(255, 255, 255, 0.4) !important;
        border-radius: 24px !important;
        padding: 28px 36px !important;
        margin: 32px 0 !important;
        display: flex !important;
        align-items: center !important;
        gap: 24px !important;
        box-shadow: 0 20px 60px -30px rgba(67, 56, 202, 0.2) !important;
        position: relative !important;
        overflow: hidden !important;
        transition: all 0.4s ease !important;
    }

    .client-banner:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 30px 80px -25px rgba(67, 56, 202, 0.3) !important;
        border-color: rgba(255, 255, 255, 0.6) !important;
    }

    /* === ADVISOR NOTES === */
    .advisor-note {
        background: linear-gradient(135deg, 
            rgba(219, 234, 254, 0.7) 0%, 
            rgba(255, 255, 255, 0.85) 100%) !important;
        backdrop-filter: blur(16px) !important;
        border: 2px solid rgba(219, 234, 254, 0.4) !important;
        border-radius: 24px !important;
        padding: 32px !important;
        margin: 32px 0 !important;
        box-shadow: 0 20px 60px -30px rgba(59, 130, 246, 0.15) !important;
    }

    /* === SCENARIO PLANNING === */
    .scenario-card {
        background: linear-gradient(135deg, 
            rgba(254, 249, 195, 0.7) 0%, 
            rgba(255, 255, 255, 0.85) 100%) !important;
        backdrop-filter: blur(16px) !important;
        border: 2px solid rgba(254, 249, 195, 0.4) !important;
        border-radius: 24px !important;
        padding: 36px !important;
        margin: 36px 0 !important;
        box-shadow: 0 20px 60px -30px rgba(245, 158, 11, 0.15) !important;
    }

    /* === VIBRANT ACTION BUTTON === */
    .stButton > button {
        height: 64px !important;
        font-size: 1.2rem !important;
        background: linear-gradient(135deg, #4338CA 0%, #6366F1 50%, #06B6D4 100%) !important;
        color: #FFFFFF !important;
        border-radius: 16px !important;
        box-shadow: 0 20px 40px -15px rgba(67, 56, 202, 0.4) !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        border: none !important;
        padding: 0 48px !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        width: 100% !important;
        position: relative !important;
        overflow: hidden !important;
    }

    .stButton > button::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 255, 255, 0.2), 
            transparent) !important;
        transition: left 0.7s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-6px) scale(1.02) !important;
        box-shadow: 0 30px 60px -20px rgba(67, 56, 202, 0.5) !important;
        background: linear-gradient(135deg, #3730A3 0%, #4F46E5 50%, #0891B2 100%) !important;
    }

    .stButton > button:hover::before {
        left: 100% !important;
    }

    /* === CUSTOM TABS === */
    .custom-tabs {
        display: flex !important;
        gap: 8px !important;
        background: rgba(255, 255, 255, 0.6) !important;
        backdrop-filter: blur(12px) !important;
        padding: 8px !important;
        border-radius: 20px !important;
        margin: 40px 0 32px !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        box-shadow: 0 12px 32px -12px rgba(0, 0, 0, 0.05) !important;
    }

    .custom-tab {
        flex: 1 !important;
        padding: 20px 32px !important;
        text-align: center !important;
        border-radius: 16px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        font-weight: 600 !important;
        color: #6B7280 !important;
        font-family: 'Outfit', sans-serif !important;
        background: transparent !important;
        font-size: 1.05rem !important;
    }

    .custom-tab:hover {
        background: rgba(255, 255, 255, 0.8) !important;
        color: #4338CA !important;
        transform: translateY(-2px) !important;
    }

    .custom-tab.active {
        background: rgba(255, 255, 255, 0.95) !important;
        color: #4338CA !important;
        font-weight: 700 !important;
        box-shadow: 0 8px 24px rgba(67, 56, 202, 0.1) !important;
        border: 2px solid rgba(67, 56, 202, 0.2) !important;
    }

    /* === STATUS BADGES === */
    .status-badge {
        display: inline-flex !important;
        align-items: center !important;
        padding: 10px 20px !important;
        border-radius: 20px !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        margin-left: 12px !important;
        font-family: 'Outfit', sans-serif !important;
        backdrop-filter: blur(8px) !important;
        border: 2px solid !important;
        transition: all 0.3s ease !important;
    }

    .badge-excellent { 
        background: rgba(67, 56, 202, 0.15) !important; 
        color: #4338CA !important; 
        border-color: rgba(67, 56, 202, 0.3) !important; 
    }

    .badge-good { 
        background: rgba(16, 185, 129, 0.15) !important; 
        color: #10B981 !important; 
        border-color: rgba(16, 185, 129, 0.3) !important; 
    }

    .badge-poor { 
        background: rgba(239, 68, 68, 0.15) !important; 
        color: #EF4444 !important; 
        border-color: rgba(239, 68, 68, 0.3) !important; 
    }

    /* === SECTION TITLES === */
    .section-title {
        font-size: 1.8rem !important;
        margin-bottom: 40px !important;
        padding-bottom: 20px !important;
        border-bottom: 2px solid rgba(30, 27, 75, 0.1) !important;
        position: relative !important;
    }

    .section-title::after {
        content: '' !important;
        position: absolute !important;
        bottom: -2px !important;
        left: 0 !important;
        width: 120px !important;
        height: 4px !important;
        background: linear-gradient(90deg, #4338CA, #6366F1, #06B6D4) !important;
        border-radius: 2px !important;
    }

    /* === RISK METER === */
    .risk-meter {
        height: 12px !important;
        background: rgba(203, 213, 225, 0.3) !important;
        border-radius: 6px !important;
        margin: 24px 0 !important;
        overflow: hidden !important;
        position: relative !important;
        backdrop-filter: blur(4px) !important;
    }

    .risk-fill {
        height: 100% !important;
        border-radius: 6px !important;
        transition: width 1s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }

    /* === COLORED ICON WRAPPERS === */
    .icon-wrapper {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        width: 48px !important;
        height: 48px !important;
        border-radius: 14px !important;
        font-size: 1.5rem !important;
        margin-right: 20px !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        backdrop-filter: blur(8px) !important;
    }

    .icon-wrapper.personal {
        background: rgba(67, 56, 202, 0.15) !important;
        color: #4338CA !important;
        border: 2px solid rgba(67, 56, 202, 0.2) !important;
    }

    .icon-wrapper.financial {
        background: rgba(139, 92, 246, 0.15) !important;
        color: #7C3AED !important;
        border: 2px solid rgba(139, 92, 246, 0.2) !important;
    }

    .icon-wrapper.credit {
        background: rgba(16, 185, 129, 0.15) !important;
        color: #10B981 !important;
        border: 2px solid rgba(16, 185, 129, 0.2) !important;
    }

    .icon-wrapper:hover {
        transform: rotate(15deg) scale(1.1) !important;
        box-shadow: 0 12px 32px -8px rgba(0, 0, 0, 0.1) !important;
    }

    /* === RESULTS REVEAL ANIMATION === */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(40px) scale(0.95);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }

    .results-section {
        animation: fadeInUp 0.8s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    /* === SCROLLBAR STYLING === */
    ::-webkit-scrollbar {
        width: 10px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb {
        background: linear-gradient(to bottom, #4338CA, #6366F1);
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(to bottom, #3730A3, #4F46E5);
    }

    /* === STYLISH PREMIUM HEADER === */
    .premium-header {
        background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.85) 0%, 
            rgba(255, 255, 255, 0.75) 100%) !important;
        backdrop-filter: blur(32px) saturate(200%) !important;
        -webkit-backdrop-filter: blur(32px) saturate(200%) !important;
        border-radius: 32px !important;
        padding: 40px 48px !important;
        border: 2px solid rgba(255, 255, 255, 0.4) !important;
        box-shadow: 
            0 40px 100px -40px rgba(67, 56, 202, 0.25),
            0 20px 40px -20px rgba(99, 102, 241, 0.15),
            inset 0 1px 0 0 rgba(255, 255, 255, 0.3) !important;
        margin: 0 0 48px 0 !important;
        position: relative !important;
        overflow: hidden !important;
    }

    .premium-header::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        height: 8px !important;
        background: linear-gradient(90deg, 
            #4338CA 0%, 
            #6366F1 25%, 
            #06B6D4 50%, 
            #10B981 75%, 
            #8B5CF6 100%) !important;
        border-radius: 32px 32px 0 0 !important;
    }

    .logo-icon {
        font-size: 3.5rem !important;
        background: linear-gradient(135deg, #4338CA, #6366F1, #06B6D4) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
        filter: drop-shadow(0 8px 16px rgba(67, 56, 202, 0.3)) !important;
        animation: float 6s ease-in-out infinite !important;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-8px) rotate(2deg); }
    }

    .floating-element {
        position: absolute !important;
        width: 80px !important;
        height: 80px !important;
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(20px) !important;
        border-radius: 50% !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        animation: float-random 15s ease-in-out infinite !important;
    }

    @keyframes float-random {
        0%, 100% { transform: translate(0, 0) rotate(0deg); }
        25% { transform: translate(20px, -15px) rotate(90deg); }
        50% { transform: translate(-15px, 10px) rotate(180deg); }
        75% { transform: translate(10px, 20px) rotate(270deg); }
    }

    .floating-element:nth-child(1) {
        top: 20% !important;
        left: 5% !important;
        background: radial-gradient(circle, rgba(67, 56, 202, 0.15), transparent 70%) !important;
    }

    .floating-element:nth-child(2) {
        bottom: 30% !important;
        right: 10% !important;
        width: 60px !important;
        height: 60px !important;
        background: radial-gradient(circle, rgba(6, 182, 212, 0.15), transparent 70%) !important;
        animation-delay: -5s !important;
    }

    .floating-element:nth-child(3) {
        top: 40% !important;
        right: 8% !important;
        width: 40px !important;
        height: 40px !important;
        background: radial-gradient(circle, rgba(139, 92, 246, 0.15), transparent 70%) !important;
        animation-delay: -10s !important;
    }

    /* Subtle Model Accuracy Indicator */
    .model-accuracy-indicator {
        position: absolute;
        top: 24px;
        right: 32px;
        font-size: 0.85rem;
        color: #6B7280;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 16px;
        border: 1px solid rgba(203, 213, 225, 0.4);
        backdrop-filter: blur(8px);
    }

    .model-accuracy-value {
        color: #7C3AED;
        font-weight: 800;
        font-size: 0.9rem;
    }
    
    /* === HTML GAUGE CHART === */
    .gauge-container {
        width: 100%;
        height: 300px;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .radar-container {
        width: 100%;
        height: 360px;
        display: flex;
        justify-content: center;
        align-items: center;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)


# --- SIMPLE HTML GAUGE FUNCTION (replaces plotly) ---
def create_html_gauge(score):
    """Create HTML gauge chart for credit score"""
    if score >= 750:
        color = "#4338CA"
        risk_level = "EXCELLENT"
        percentage = 88
    elif score >= 650:
        color = "#10B981"
        risk_level = "GOOD"
        percentage = 65
    else:
        color = "#EF4444"
        risk_level = "NEEDS IMPROVEMENT"
        percentage = 35
    
    return f'''
    <div class="gauge-container">
        <div style="text-align: center; width: 100%;">
            <div style="font-size: 1.1rem; color: #6B7280; margin-bottom: 10px; font-weight: 600;">CREDIT SCORE</div>
            <div style="font-size: 0.9rem; color: {color}; font-weight: 700; margin-bottom: 20px; padding: 8px 16px; background: {color}15; border-radius: 20px; display: inline-block;">{risk_level}</div>
            <div style="font-size: 4.5rem; font-weight: 800; color: {color}; margin: 20px 0; line-height: 1;">{score}</div>
            
            <div style="width: 90%; max-width: 500px; margin: 30px auto;">
                <div style="width: 100%; height: 24px; background: linear-gradient(90deg, 
                    #EF4444 0%, 
                    #F59E0B 25%, 
                    #10B981 50%, 
                    #3B82F6 75%, 
                    #4338CA 100%); 
                    border-radius: 12px; 
                    margin-bottom: 10px;"></div>
                
                <div style="display: flex; justify-content: space-between; width: 100%;">
                    <span style="font-size: 0.85rem; color: #6B7280; font-weight: 600;">300</span>
                    <span style="font-size: 0.85rem; color: #6B7280; font-weight: 600;">400</span>
                    <span style="font-size: 0.85rem; color: #6B7280; font-weight: 600;">500</span>
                    <span style="font-size: 0.85rem; color: #6B7280; font-weight: 600;">600</span>
                    <span style="font-size: 0.85rem; color: #6B7280; font-weight: 600;">700</span>
                    <span style="font-size: 0.85rem; color: #6B7280; font-weight: 600;">800</span>
                    <span style="font-size: 0.85rem; color: #6B7280; font-weight: 600;">850</span>
                </div>
                
                <div style="margin-top: 25px; position: relative;">
                    <div style="position: absolute; left: {percentage}%; transform: translateX(-50%); bottom: 0;">
                        <div style="width: 2px; height: 30px; background: {color};"></div>
                        <div style="width: 20px; height: 20px; background: {color}; border-radius: 50%; margin-top: -10px; margin-left: -9px;"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    '''

# --- SIMPLE RADAR CHART FUNCTION (replaces plotly) ---
def create_simple_radar_chart(utilization, delinquency, loan_to_income, age, income_score):
    """Create HTML radar chart"""
    # Calculate scores
    util_score = max(10, 100 - utilization * 0.8)
    delinq_score = max(10, 100 - delinquency * 1.2)
    lti_score = max(10, 100 - min(loan_to_income * 0.8, 90))
    age_score = max(10, min(age * 1.5, 90)) if age < 65 else max(10, 100 - (age - 65) * 2)
    inc_score = max(10, min(income_score, 90))
    
    scores = [util_score, delinq_score, lti_score, age_score, inc_score]
    categories = ['Credit Utilization', 'Payment History', 'Loan-to-Income', 'Age Factor', 'Income Level']
    
    # Create radar chart HTML
    radar_html = '''
    <div class="radar-container">
        <div style="width: 100%; height: 100%; position: relative;">
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 280px; height: 280px; border-radius: 50%; border: 2px solid rgba(203, 213, 225, 0.5);"></div>
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 220px; height: 220px; border-radius: 50%; border: 2px solid rgba(203, 213, 225, 0.4);"></div>
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 160px; height: 160px; border-radius: 50%; border: 2px solid rgba(203, 213, 225, 0.3);"></div>
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 100px; height: 100px; border-radius: 50%; border: 2px solid rgba(203, 213, 225, 0.2);"></div>
    '''
    
    # Add data points
    for i, (score, category) in enumerate(zip(scores, categories)):
        angle = (i * 72 - 90) * 3.14159 / 180
        radius = (score / 100) * 140  # 140 is max radius
        
        x = 50 + radius * np.cos(angle) / 140 * 100
        y = 50 + radius * np.sin(angle) / 140 * 100
        
        # Add point
        radar_html += f'''
        <div style="position: absolute; top: {y}%; left: {x}%; transform: translate(-50%, -50%);">
            <div style="width: 12px; height: 12px; background: #7C3AED; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 8px rgba(124, 58, 237, 0.3);"></div>
            <div style="position: absolute; top: 20px; left: 50%; transform: translateX(-50%); white-space: nowrap; font-size: 0.8rem; color: #1E1B4B; font-weight: 600; background: rgba(255,255,255,0.9); padding: 4px 8px; border-radius: 10px; border: 1px solid rgba(203,213,225,0.3);">
                {category}<br><span style="color: #7C3AED; font-weight: 800;">{int(score)}/100</span>
            </div>
        </div>
        '''
    
    # Close container
    radar_html += '''
        </div>
    </div>
    '''
    
    return radar_html, {
        'utilization': util_score,
        'delinquency': delinq_score,
        'loan_to_income': lti_score,
        'age': age_score,
        'income': inc_score
    }

# --- HELPER FUNCTIONS ---
def calculate_potential_score(current_score, changes):
    """Calculate potential score improvement"""
    potential = current_score

    # Income improvement
    income_impact = min(changes.get('income_pct', 0) * 0.8, 40)
    potential += income_impact

    # Utilization improvement
    util_change = max(changes.get('utilization_current', 30) - changes.get('utilization_target', 30), 0)
    util_impact = min(util_change * 1.2, 60)
    potential += util_impact

    # Loan amount adjustment
    loan_impact = min(max(changes.get('loan_adjustment', 0), -30), 0)
    potential += loan_impact

    return min(potential, 850), {
        'income_impact': income_impact,
        'util_impact': util_impact,
        'loan_impact': loan_impact,
        'total_improvement': income_impact + util_impact + loan_impact
    }


# --- SESSION STATE ---
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = 'overview'

# --- PREMIUM HEADER SECTION ---
st.markdown('<div class="premium-header">', unsafe_allow_html=True)

# Floating background elements
st.markdown(
    '<div class="floating-element"></div><div class="floating-element"></div><div class="floating-element"></div>',
    unsafe_allow_html=True)

# Subtle model accuracy indicator in top right corner
st.markdown("""
<div class="model-accuracy-indicator">
    <span>⚡</span>
    <span>Model Accuracy:</span>
    <span class="model-accuracy-value">99.1%</span>
</div>
""", unsafe_allow_html=True)

# Clean header centered design
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <div style="display: flex; align-items: center; justify-content: center; gap: 20px; margin-bottom: 16px;">
            <div class="logo-icon">💎</div>
            <div>
                <div style="font-size: 3rem; font-weight: 900; letter-spacing: -1.5px; background: linear-gradient(135deg, #4338CA 0%, #3730A3 50%, #1E1B4B 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-family: 'Outfit', sans-serif;">
                    ELITECREDIT
                </div>
                <div style="font-size: 1.3rem; font-weight: 700; color: #6366F1; margin-top: 4px;">
                    Advisor Intelligence Platform
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div style="font-size: 1.1rem; color: #6B7280; font-weight: 600; margin-top: 8px; text-align: center;">AI-Powered Credit Assessment System</div>',
        unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Main Container
with st.container():
    st.markdown('<div class="premium-container">', unsafe_allow_html=True)

    # Custom Tabs
    col1, col2, col3 = st.columns(3)
    with col1:
        overview_active = "active" if st.session_state.current_tab == 'overview' else ""
        st.markdown(f'<div class="custom-tab {overview_active}">📊 Overview</div>', unsafe_allow_html=True)
    with col2:
        scenario_active = "active" if st.session_state.current_tab == 'scenario' else ""
        st.markdown(f'<div class="custom-tab {scenario_active}">🔄 Scenario Planning</div>', unsafe_allow_html=True)
    with col3:
        details_active = "active" if st.session_state.current_tab == 'details' else ""
        st.markdown(f'<div class="custom-tab {details_active}">🔍 Detailed Analysis</div>', unsafe_allow_html=True)

    # Input Section
    st.markdown('<div class="section-title" style="color: #1E1B4B !important;">📋 Client Profile Assessment</div>',
                unsafe_allow_html=True)

    # Form in two columns with color-coded themes
    form_col1, form_col2 = st.columns(2)

    with form_col1:
        st.markdown('<div class="form-card personal">', unsafe_allow_html=True)
        st.markdown(
            '<div class="form-header personal"><span class="icon-wrapper personal">👤</span> Personal Information</div>',
            unsafe_allow_html=True)

        age = st.number_input('Applicant Age', min_value=18, max_value=100, value=32,
                              help="Age of the primary applicant")

        residence_type = st.selectbox(
            'Residence Type',
            ['Owned', 'Mortgage', 'Rented', 'With Family'],
            help="Current living arrangement"
        )

        employment_status = st.selectbox(
            'Employment Status',
            ['Full-time', 'Self-employed', 'Contract', 'Part-time', 'Retired'],
            help="Current employment situation"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with form_col2:
        st.markdown('<div class="form-card financial">', unsafe_allow_html=True)
        st.markdown(
            '<div class="form-header financial"><span class="icon-wrapper financial">💰</span> Financial Capacity</div>',
            unsafe_allow_html=True)

        annual_income = st.number_input(
            'Annual Income (₹)',
            min_value=0,
            value=1200000,
            step=50000,
            format="%d",
            help="Gross annual income"
        )

        loan_amount = st.number_input(
            'Desired Loan Amount (₹)',
            min_value=0,
            value=5000000,
            step=100000,
            format="%d",
            help="Requested loan amount"
        )

        loan_tenure = st.slider(
            'Loan Tenure (Months)',
            min_value=12,
            max_value=360,
            value=36,
            step=12,
            help="Preferred loan duration"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # Credit Information - Emerald Theme
    st.markdown('<div class="form-card credit">', unsafe_allow_html=True)
    st.markdown('<div class="form-header credit"><span class="icon-wrapper credit">📊</span> Credit History</div>',
                unsafe_allow_html=True)

    col_credit1, col_credit2, col_credit3 = st.columns(3)

    with col_credit1:
        credit_utilization = st.slider(
            'Credit Utilization (%)',
            min_value=0,
            max_value=100,
            value=35,
            help="Percentage of available credit currently in use"
        )

    with col_credit2:
        delinquency_ratio = st.slider(
            'Delinquency Ratio (%)',
            min_value=0,
            max_value=100,
            value=10,
            help="Percentage of accounts with late payments"
        )

    with col_credit3:
        avg_dpd = st.number_input(
            'Avg Days Past Due',
            min_value=0,
            max_value=365,
            value=5,
            help="Average days late on payments"
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # VIBRANT ANALYSIS BUTTON
    st.markdown("<div style='margin: 48px 0;'>", unsafe_allow_html=True)
    analyze_clicked = st.button(
        "🚀 GENERATE COMPREHENSIVE CREDIT ASSESSMENT",
        use_container_width=True,
        type="primary",
        key="analyze_btn"
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if analyze_clicked:
        st.session_state.analysis_complete = True

        # Calculate additional metrics
        loan_to_income = (loan_amount / annual_income * 100) if annual_income > 0 else 0
        monthly_emi = loan_amount / loan_tenure if loan_tenure > 0 else 0
        debt_to_income = (monthly_emi * 12 / annual_income * 100) if annual_income > 0 else 0

        # Get prediction
        prob, score, rating = predict(
            age=age,
            income=annual_income,
            loan_amount=loan_amount,
            loan_tenure_months=loan_tenure,
            avg_dpd_per_delinquency=avg_dpd,
            delinquency_ratio=delinquency_ratio,
            credit_utilization_ratio=credit_utilization,
            num_open_accounts=2,
            residence_type=residence_type,
            loan_purpose="Home",
            loan_type="Unsecured"
        )

        # Store in session state
        st.session_state.prediction_results = {
            'probability': prob,
            'credit_score': score,
            'rating': rating,
            'loan_to_income': loan_to_income,
            'debt_to_income': debt_to_income,
            'monthly_emi': monthly_emi,
            'raw_inputs': {
                'age': age,
                'annual_income': annual_income,
                'loan_amount': loan_amount,
                'credit_utilization': credit_utilization,
                'delinquency_ratio': delinquency_ratio
            }
        }

        st.rerun()

    if st.session_state.get('analysis_complete', False):
        results = st.session_state.prediction_results

        # CLIENT PROFILE BANNER
        if results['credit_score'] >= 750:
            banner_class = "tier-1"
            banner_title = "💎 TIER-1 ELITE CLIENT"
            banner_color = "#4338CA"
            banner_icon = "💎"
            banner_subtitle = "Premium service level • Fast-track processing • Priority support"
        elif results['credit_score'] >= 650:
            banner_class = "tier-2"
            banner_title = "⭐ TIER-2 STANDARD CLIENT"
            banner_color = "#10B981"
            banner_icon = "⭐"
            banner_subtitle = "Standard service level • Enhanced verification • Regular monitoring"
        else:
            banner_class = "tier-3"
            banner_title = "📝 TIER-3 DEVELOPING CLIENT"
            banner_color = "#EF4444"
            banner_icon = "📝"
            banner_subtitle = "Development program • Close monitoring • Financial guidance"

        st.markdown(f"""
        <div class="client-banner results-section">
            <div style="font-size: 2.5rem; color: {banner_color} !important;">{banner_icon}</div>
            <div style="flex: 1;">
                <h3 style="margin: 0; color: {banner_color} !important; font-weight: 800; font-size: 1.5rem;">{banner_title}</h3>
                <p style="margin: 8px 0 0 0; color: #6B7280 !important; font-size: 1.05rem; font-weight: 500;">{banner_subtitle}</p>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 0.95rem; color: #6B7280 !important; font-weight: 600;">Client Reference</div>
                <div style="font-size: 1.4rem; font-weight: 800; color: #1E1B4B !important; letter-spacing: 1px;">CR-{datetime.now().strftime('%H%M')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
        st.markdown(
            '<div class="section-title results-section" style="color: #1E1B4B !important;">📈 Assessment Results</div>',
            unsafe_allow_html=True)

        # Score Spotlight
        col_score, col_metrics = st.columns([1, 2])

        with col_score:
            st.markdown("<div class='score-spotlight results-section'>", unsafe_allow_html=True)

            # Determine score class
            if results['credit_score'] >= 750:
                score_class = "score-excellent"
                score_color = "#4338CA"
                badge_class = "badge-excellent"
                badge_text = "EXCELLENT"
                score_label = "Elite Credit Standing"
            elif results['credit_score'] >= 650:
                score_class = "score-good"
                score_color = "#10B981"
                badge_class = "badge-good"
                badge_text = "GOOD"
                score_label = "Strong Credit Profile"
            else:
                score_class = "score-poor"
                score_color = "#EF4444"
                badge_class = "badge-poor"
                badge_text = "DEVELOPMENT AREA"
                score_label = "Growth Opportunity"

            # Score Circle
            st.markdown(f"""
            <div class="score-circle {score_class}">
                <span style="color: #6B7280 !important; font-size: 0.95rem; font-weight: 700; letter-spacing: 0.05em; margin-bottom: 8px;">CREDIT SCORE</span>
                <span style="font-size: 3.8rem; font-weight: 800; color: {score_color} !important; margin: 12px 0; line-height: 1;">{results['credit_score']}</span>
                <span style="font-size: 1.2rem; font-weight: 700; color: {score_color} !important; margin-top: 8px;">
                    {results['rating']} RATING
                </span>
                <div style="margin-top: 16px; font-size: 0.9rem; color: #6B7280 !important; font-weight: 600; padding: 8px 16px; background: rgba(255,255,255,0.5); border-radius: 20px;">
                    {score_label}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Risk Meter
            risk_percentage = min(results['probability'] * 100, 100)
            risk_color = "#4338CA" if results['probability'] < 0.1 else "#10B981" if results['probability'] < 0.25 else "#EF4444"

            # Calculate risk level
            risk_level_index = int(results['probability'] > 0.1) + int(results['probability'] > 0.25)
            risk_levels = ["Low Risk", "Moderate Risk", "High Risk"]
            current_risk = risk_levels[risk_level_index]

            st.markdown(f"""
            <div style="margin-top: 40px; padding: 28px; background: rgba(255, 255, 255, 0.9) !important; backdrop-filter: blur(16px); border-radius: 24px; border: 2px solid rgba(255, 255, 255, 0.4) !important; box-shadow: 0 20px 60px -30px rgba(67, 56, 202, 0.15);">
                <div style="display: flex; justify-content: space-between; margin-bottom: 20px; align-items: center;">
                    <span style="color: #1E1B4B !important; font-size: 1.1rem; font-weight: 700;">Default Probability</span>
                    <span style="font-weight: 800; color: {risk_color} !important; font-size: 1.4rem; background: rgba(255,255,255,0.9); padding: 8px 20px; border-radius: 24px; border: 3px solid {risk_color}22;">{results['probability']:.1%}</span>
                </div>
                <div class="risk-meter">
                    <div class="risk-fill" style="width: {risk_percentage}%; background: {risk_color} !important;"></div>
                </div>
                <div style="display: flex; justify-content: space-between; margin-top: 16px;">
                    <span style="font-size: 1rem; color: #6B7280 !important; font-weight: 600;">Risk Assessment:</span>
                    <span style="font-size: 1.05rem; color: {risk_color} !important; font-weight: 800;">{current_risk}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

        with col_metrics:
            # COLOR-CODED METRIC CARDS WITH UNIQUE IDENTITIES
            st.markdown("<div style='margin-bottom: 32px;' class='results-section'>", unsafe_allow_html=True)
            metric_cols = st.columns(3)

            with metric_cols[0]:
                lti_status = "Optimal" if results['loan_to_income'] < 30 else "Moderate" if results['loan_to_income'] < 50 else "High"
                lti_color = "#4338CA" if results['loan_to_income'] < 30 else "#6366F1" if results['loan_to_income'] < 50 else "#7C3AED"
                st.markdown(f"""
                <div class="metric-card lti">
                    <div class="metric-label">Loan-to-Income Ratio</div>
                    <div class="metric-value" style="background: linear-gradient(135deg, {lti_color}, #6366F1) !important; -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important;">{results['loan_to_income']:.1f}%</div>
                    <div class="metric-subtitle" style="color: {lti_color} !important; font-weight: 700;">{lti_status}</div>
                </div>
                """, unsafe_allow_html=True)

            with metric_cols[1]:
                dti_status = "Affordable" if results['debt_to_income'] < 20 else "Manageable" if results['debt_to_income'] < 35 else "Elevated"
                dti_color = "#7C3AED" if results['debt_to_income'] < 20 else "#8B5CF6" if results['debt_to_income'] < 35 else "#A78BFA"
                st.markdown(f"""
                <div class="metric-card dti">
                    <div class="metric-label">Debt Service Ratio</div>
                    <div class="metric-value" style="background: linear-gradient(135deg, {dti_color}, #A78BFA) !important; -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important;">{results['debt_to_income']:.1f}%</div>
                    <div class="metric-subtitle" style="color: {dti_color} !important; font-weight: 700;">{dti_status}</div>
                </div>
                """, unsafe_allow_html=True)

            with metric_cols[2]:
                emi_formatted = f"₹{results['monthly_emi']:,.0f}"
                emi_color = "#06B6D4" if results['monthly_emi'] < 50000 else "#0891B2" if results['monthly_emi'] < 100000 else "#0E7490"
                st.markdown(f"""
                <div class="metric-card emi">
                    <div class="metric-label">Monthly EMI</div>
                    <div class="metric-value" style="background: linear-gradient(135deg, {emi_color}, #22D3EE) !important; -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important;">{emi_formatted}</div>
                    <div class="metric-subtitle" style="color: {emi_color} !important; font-weight: 700;">Estimated Payment</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # HTML RADAR CHART
            st.markdown("<div class='results-section'>", unsafe_allow_html=True)
            st.markdown(
                "<h4 style='color: #1E1B4B !important; margin-bottom: 24px; font-size: 1.4rem;'>📊 Risk Factor Analysis</h4>",
                unsafe_allow_html=True)

            # Calculate income score
            income_score = max(10, min(annual_income / 5000000 * 100, 90))

            # Create vibrant radar chart
            radar_html, radar_scores = create_simple_radar_chart(
                credit_utilization,
                delinquency_ratio,
                results['loan_to_income'],
                age,
                income_score
            )

            st.markdown(radar_html, unsafe_allow_html=True)

            # Radar insights
            st.markdown(
                "<div style='margin-top: 24px; padding: 24px; background: rgba(255, 255, 255, 0.8) !important; backdrop-filter: blur(16px); border-radius: 20px; border: 2px solid rgba(219, 234, 254, 0.4) !important;'>",
                unsafe_allow_html=True)
            st.markdown(
                "<p style='margin: 0; color: #1E1B4B !important; font-weight: 700; font-size: 1.1rem;'>💡 Key Insight: ",
                unsafe_allow_html=True)

            lowest_factor = min(radar_scores, key=radar_scores.get)
            if lowest_factor == 'utilization':
                st.markdown(
                    "<span style='color: #6B7280 !important; font-weight: 500;'>Credit utilization is the primary area for improvement. Reducing this below 30% would unlock better terms.</span>",
                    unsafe_allow_html=True)
            elif lowest_factor == 'delinquency':
                st.markdown(
                    "<span style='color: #6B7280 !important; font-weight: 500;'>Payment history needs attention. Consistent on-time payments will substantially improve creditworthiness.</span>",
                    unsafe_allow_html=True)
            else:
                st.markdown(
                    "<span style='color: #6B7280 !important; font-weight: 500;'>Overall profile is promising. Focus on maintaining financial discipline while optimizing key areas.</span>",
                    unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # ADVISOR NOTES
            st.markdown("<div class='advisor-note results-section'>", unsafe_allow_html=True)
            st.markdown("<h4 style='margin-top: 0; color: #1E1B4B !important; font-size: 1.4rem;'>💡 Advisor Notes</h4>",
                        unsafe_allow_html=True)

            if results['credit_score'] >= 750:
                st.markdown("""
                <div style='color: #1E1B4B !important; line-height: 1.7;'>
                    <strong style='color: #4338CA !important;'>Elite Profile Detected</strong> - This client qualifies for premium treatment:
                    <ul style='margin: 16px 0 16px 20px; padding-left: 0;'>
                        <li><strong>Interest Rates:</strong> 7-9% p.a. (Preferential rates)</li>
                        <li><strong>Processing:</strong> Fast-track with priority handling</li>
                        <li><strong>Loan Amount:</strong> Up to 90% of property value</li>
                        <li><strong>Fees:</strong> Processing fees waived entirely</li>
                        <li><strong>Support:</strong> Dedicated relationship manager</li>
                    </ul>
                    <strong style='color: #4338CA !important;'>Recommendation:</strong> Present the premium package and expedite approval.
                </div>
                """, unsafe_allow_html=True)
            elif results['credit_score'] >= 650:
                st.markdown("""
                <div style='color: #1E1B4B !important; line-height: 1.7;'>
                    <strong style='color: #10B981 !important;'>Solid Foundation</strong> - Consider these strategies:
                    <ul style='margin: 16px 0 16px 20px; padding-left: 0;'>
                        <li><strong>Interest Rates:</strong> 10-12% p.a. (Standard market rates)</li>
                        <li><strong>Verification:</strong> Additional income documentation</li>
                        <li><strong>Co-applicant:</strong> Recommend co-signer with 700+ score</li>
                        <li><strong>Monitoring:</strong> Quarterly credit review</li>
                        <li><strong>Timeline:</strong> Standard 7-10 business day processing</li>
                    </ul>
                    <strong style='color: #10B981 !important;'>Recommendation:</strong> Standard package with 6-month review clause.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style='color: #1E1B4B !important; line-height: 1.7;'>
                    <strong style='color: #EF4444 !important;'>Growth Opportunity</strong> - Focus on foundational improvements:
                    <ul style='margin: 16px 0 16px 20px; padding-left: 0;'>
                        <li><strong>Immediate Action:</strong> Reduce credit utilization below 30%</li>
                        <li><strong>Payment Strategy:</strong> Clear any delinquent accounts</li>
                        <li><strong>Product Recommendation:</strong> Secured credit card options</li>
                        <li><strong>Timeline:</strong> 12-month rebuilding plan</li>
                        <li><strong>Alternative:</strong> Consider guarantor options</li>
                    </ul>
                    <strong style='color: #EF4444 !important;'>Recommendation:</strong> Credit building program with gradual access.
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # SCENARIO PLANNING SECTION
        st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
        st.markdown(
            '<div class="section-title results-section" style="color: #1E1B4B !important;">🔄 Scenario Planning</div>',
            unsafe_allow_html=True)

        st.markdown("""
        <div class="scenario-card results-section">
            <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 24px;">
                <div style="font-size: 2.2rem; color: #F59E0B;">🎯</div>
                <div>
                    <h4 style="margin: 0; color: #92400E !important; font-size: 1.5rem;">Optimization Opportunities</h4>
                    <p style="margin: 8px 0 0 0; color: #92400E !important; font-weight: 500; font-size: 1.05rem;">
                        Adjust variables below to demonstrate how financial improvements could unlock better terms for your client.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        scenario_col1, scenario_col2 = st.columns(2)

        with scenario_col1:
            st.markdown('<div class="form-card results-section">', unsafe_allow_html=True)
            st.markdown('<div class="form-header"><span class="icon-wrapper">📈</span> Improvement Scenarios</div>',
                        unsafe_allow_html=True)

            income_increase = st.slider(
                'Income Increase (%)',
                min_value=0,
                max_value=50,
                value=0,
                help="Demonstrate the impact of potential salary growth or additional income"
            )

            utilization_target = st.slider(
                'Target Credit Utilization (%)',
                min_value=0,
                max_value=100,
                value=min(credit_utilization, 25),
                help="Show benefits of reducing credit card usage"
            )

            st.markdown(
                "<div style='margin-top: 24px; padding: 20px; background: rgba(255, 251, 235, 0.5); border-radius: 16px; border: 2px dashed #FDE68A;'>",
                unsafe_allow_html=True)
            st.markdown("<p style='margin: 0; color: #92400E !important; font-size: 0.95rem; font-weight: 600;'>",
                        unsafe_allow_html=True)
            st.markdown(
                "💡 <strong>Quick Optimization:</strong> Set utilization to 20% to show maximum potential improvement.",
                unsafe_allow_html=True)
            st.markdown("</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

        with scenario_col2:
            st.markdown('<div class="form-card results-section">', unsafe_allow_html=True)
            st.markdown('<div class="form-header"><span class="icon-wrapper">🎯</span> Potential Impact</div>',
                        unsafe_allow_html=True)

            # Calculate potential improvements
            current_score = results['credit_score']
            changes = {
                'income_pct': income_increase,
                'utilization_current': credit_utilization,
                'utilization_target': utilization_target,
                'loan_adjustment': 0
            }

            potential_score, impacts = calculate_potential_score(current_score, changes)
            score_improvement = impacts['total_improvement']

            # Display current vs potential with vibrant styling
            col_current, col_potential = st.columns(2)
            with col_current:
                st.markdown(f"""
                <div style='text-align: center; padding: 24px; background: linear-gradient(135deg, rgba(219, 234, 254, 0.5), rgba(255, 255, 255, 0.8)); border-radius: 20px; border: 3px solid rgba(67, 56, 202, 0.3);'>
                    <div style='font-size: 1rem; color: #4338CA !important; margin-bottom: 12px; font-weight: 700;'>CURRENT SCORE</div>
                    <div style='font-size: 2.4rem; font-weight: 800; color: #4338CA !important;'>{current_score}</div>
                    <div style='font-size: 0.9rem; color: #6B7280 !important; margin-top: 8px; font-weight: 600;'>As-Is Profile</div>
                </div>
                """, unsafe_allow_html=True)

            with col_potential:
                improvement_color = "#4338CA" if score_improvement > 30 else "#10B981" if score_improvement > 15 else "#6B7280"
                st.markdown(f"""
                <div style='text-align: center; padding: 24px; background: linear-gradient(135deg, rgba(219, 250, 254, 0.5), rgba(255, 255, 255, 0.8)); border-radius: 20px; border: 3px solid rgba(6, 182, 212, 0.3);'>
                    <div style='font-size: 1rem; color: #06B6D4 !important; margin-bottom: 12px; font-weight: 700;'>POTENTIAL SCORE</div>
                    <div style='font-size: 2.4rem; font-weight: 800; color: #06B6D4 !important;'>{potential_score:.0f}</div>
                    <div style='font-size: 0.9rem; color: #06B6D4 !important; margin-top: 8px; font-weight: 600;'>Optimized Profile</div>
                </div>
                """, unsafe_allow_html=True)

            # IMPROVEMENT METER
            improvement_percentage = (score_improvement / 850) * 100
            st.markdown(f"""
            <div style='margin: 32px 0; padding: 28px; background: linear-gradient(135deg, rgba(255, 251, 235, 0.6), rgba(255, 255, 255, 0.8)); border-radius: 24px; border: 2px solid #FDE68A; text-align: center; box-shadow: 0 20px 60px -30px rgba(245, 158, 11, 0.2);'>
                <div style='font-size: 1.1rem; color: #92400E !important; margin-bottom: 16px; font-weight: 700;'>POTENTIAL SCORE IMPROVEMENT</div>
                <div style='font-size: 3.2rem; font-weight: 800; color: #F59E0B !important; margin: 16px 0; text-shadow: 0 4px 12px rgba(245, 158, 11, 0.2);'>+{score_improvement:.0f} POINTS</div>
                <div style='height: 14px; background: rgba(245, 158, 11, 0.2); border-radius: 7px; margin: 24px 0; overflow: hidden;'>
                    <div style='height: 100%; width: {improvement_percentage}%; background: linear-gradient(90deg, #F59E0B, #D97706); border-radius: 7px; transition: width 0.6s ease;'></div>
                </div>
                <div style='font-size: 1.2rem; color: #92400E !important; font-weight: 700;'>
                    {score_improvement:.0f} points could unlock better interest rates and terms
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("**Impact Breakdown:**")
            col_imp1, col_imp2, col_imp3 = st.columns(3)
            with col_imp1:
                st.metric("Income Impact", f"+{impacts['income_impact']:.0f} pts",
                          delta="Significant" if impacts['income_impact'] > 20 else "Moderate" if impacts['income_impact'] > 10 else "Minimal",
                          delta_color="normal")
            with col_imp2:
                st.metric("Utilization Impact", f"+{impacts['util_impact']:.0f} pts",
                          delta="High Impact" if impacts['util_impact'] > 30 else "Moderate" if impacts['util_impact'] > 15 else "Low",
                          delta_color="normal")
            with col_imp3:
                st.metric("Loan Terms", f"{impacts['loan_impact']:.0f} pts",
                          delta="Neutral" if impacts['loan_impact'] == 0 else "Negative",
                          delta_color="inverse" if impacts['loan_impact'] < 0 else "normal")

            st.markdown("---")

            if score_improvement > 0:
                interest_rate_improvement = min(score_improvement * 0.05, 2.5)
                st.success(f"""
                **🎯 Client Meeting Talking Points:**

                "Based on our analysis, if we work together to reduce your credit utilization from **{credit_utilization}%** to **{utilization_target}%**, your credit score could improve by **{score_improvement:.0f} points**.

                This improvement could potentially:
                - **Reduce your interest rate** by up to **{interest_rate_improvement:.1f}%**
                - **Save approximately ₹{(loan_amount * interest_rate_improvement / 100 * loan_tenure / 12):,.0f}** in interest over the loan term
                - **Improve loan approval chances** for future applications

                Would you like to discuss a specific action plan to achieve these improvements?"
                """)
            else:
                st.info("""
                **📊 Relationship Manager Insight:**

                While there's limited immediate improvement potential, focusing on long-term financial discipline is key. 
                Consider discussing:
                - Credit utilization management strategies
                - Income diversification opportunities
                - Regular credit monitoring services

                Building a strong financial foundation now will unlock better opportunities in the future.
                """)

            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# VIBRANT FOOTER
st.markdown("""
<div style="text-align: center; margin-top: 80px; padding: 40px; color: #6B7280 !important; font-size: 0.95rem; background: rgba(255, 255, 255, 0.8) !important; backdrop-filter: blur(20px); border-radius: 28px; border: 2px solid rgba(255, 255, 255, 0.4) !important; box-shadow: 0 30px 80px -20px rgba(67, 56, 202, 0.1);">
    <p style="margin: 0 0 16px 0; font-family: 'Outfit', sans-serif; font-weight: 700; font-size: 1.2rem; color: #1E1B4B !important;">
        EliteCredit Advisor Portal v4.4 | <span style="background: linear-gradient(90deg, #4338CA, #6366F1, #06B6D4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;">Jewel-Tone Professional</span>
    </p>
    <p style="margin: 0; font-size: 0.9rem; color: #6B7280 !important; max-width: 900px; margin: 12px auto; line-height: 1.7; font-weight: 500;">
        This vibrant interface combines deep navy readability with jewel-tone aesthetics to create a high-end, 
        professional fintech experience designed for modern relationship management and client consultations.
    </p>
    <div style="margin-top: 28px; display: flex; justify-content: center; gap: 40px; font-size: 0.85rem; color: #9CA3AF !important; font-weight: 600;">
        <span style="color: #4338CA !important;">🔐 ISO 27001 Certified</span>
        <span style="color: #10B981 !important;">📊 Real-time Analytics</span>
        <span style="color: #6366F1 !important;">🤖 AI-Powered Insights</span>
        <span style="color: #06B6D4 !important;">👥 Client-Centric Design</span>
        <span style="color: #8B5CF6 !important;">🎨 Vibrant Professional UI</span>
    </div>
</div>
""", unsafe_allow_html=True)
