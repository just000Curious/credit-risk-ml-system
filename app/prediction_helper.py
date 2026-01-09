# prediction_helper.py - Simple version without joblib
import numpy as np

def predict(age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
            delinquency_ratio, credit_utilization_ratio, num_open_accounts,
            residence_type, loan_purpose, loan_type):
    """Simple credit score calculator - NO JOBLIB"""
    
    # Base score calculation
    base_score = 650
    
    # Age factor
    if age < 25:
        base_score -= 20
    elif 25 <= age <= 35:
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
