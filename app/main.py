"""
EliteCredit Advisor Portal
Entry point for the professional credit risk assessment application.
"""
import streamlit as st

# Configure the page before importing anything else
st.set_page_config(
    page_title="EliteCredit | Advisor Portal",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

from styles.theme import get_css
from components.header import render_header
from pages.assessment import render_input_form, render_results
from pages.scenario import render_scenario_planner
from prediction_helper import predict


def main():
    # ── Apply Design System ──
    st.markdown(get_css(), unsafe_allow_html=True)
    
    # ── Render Header ──
    render_header()
    
    # ── Initialize Session State ──
    if 'analysis_complete' not in st.session_state:
        st.session_state.analysis_complete = False
    
    # ── Sidebar Navigation & Actions ──
    with st.sidebar:
        st.markdown("""
        <div style="font-size: 1.2rem; font-weight: 700; margin-bottom: 24px; color: #F1F5F9;">
            ⬡ EliteCredit
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div style="font-size: 0.75rem; font-weight: 600; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 12px;">Navigation</div>', unsafe_allow_html=True)
        
        page = st.radio(
            "Select Page",
            ["Dashboard", "Assessment", "Scenario Planning", "Settings"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        if st.button("Reset Assessment", use_container_width=True):
            st.session_state.analysis_complete = False
            if 'prediction_results' in st.session_state:
                del st.session_state.prediction_results
            st.rerun()
            
        st.markdown("""
        <div style="position: absolute; bottom: 20px; font-size: 0.7rem; color: #64748B;">
            v2.1 Enterprise Build<br>
            ISO 27001 Certified
        </div>
        """, unsafe_allow_html=True)

    # ── Main Content Area ──
    if page == "Dashboard":
        st.markdown("### System Dashboard")
        st.info("System operational. Navigate to **Assessment** to evaluate a new client.")
        
    elif page == "Settings":
        st.markdown("### Model Settings")
        st.info("Configuration options are restricted to admin users.")
        
    elif page in ["Assessment", "Scenario Planning"]:
        # We handle the primary user flow here
        
        # 1. Collect inputs
        raw_inputs = render_input_form()
        
        # 2. Analyze Button
        st.markdown("<div style='margin: 32px 0 16px;'></div>", unsafe_allow_html=True)
        if st.button("Generate Credit Assessment", type="primary", use_container_width=True):
            with st.spinner("Analyzing credit profile..."):
                # Calculate derived metrics
                annual_income = raw_inputs['annual_income']
                loan_amount = raw_inputs['loan_amount']
                loan_tenure = raw_inputs['loan_tenure']
                
                loan_to_income = (loan_amount / annual_income * 100) if annual_income > 0 else 0
                monthly_emi = loan_amount / loan_tenure if loan_tenure > 0 else 0
                debt_to_income = (monthly_emi * 12 / annual_income * 100) if annual_income > 0 else 0
                
                # Run prediction model
                prob, score, rating = predict(
                    raw_inputs['age'], 
                    annual_income, 
                    loan_amount, 
                    loan_tenure,
                    raw_inputs['avg_dpd'], 
                    raw_inputs['delinquency_ratio'], 
                    raw_inputs['credit_utilization'],
                    2, # dummy num_open_accounts
                    raw_inputs['residence_type'], 
                    "Home", # dummy loan_purpose
                    "Secured" # dummy loan_type
                )
                
                st.session_state.prediction_results = {
                    'probability': prob,
                    'credit_score': score,
                    'rating': rating,
                    'loan_to_income': loan_to_income,
                    'debt_to_income': debt_to_income,
                    'monthly_emi': monthly_emi
                }
                st.session_state.raw_inputs = raw_inputs
                st.session_state.analysis_complete = True
                
        # 3. Show Results or Scenario Planner based on page selection
        if st.session_state.analysis_complete:
            st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True)
            
            if page == "Assessment":
                render_results(st.session_state.prediction_results, st.session_state.raw_inputs)
            elif page == "Scenario Planning":
                render_scenario_planner(st.session_state.prediction_results, st.session_state.raw_inputs)


if __name__ == "__main__":
    main()
