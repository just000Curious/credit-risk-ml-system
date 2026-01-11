import numpy as np
import pandas as pd

def predict(age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
            delinquency_ratio, credit_utilization_ratio, num_open_accounts,
            residence_type, loan_purpose, loan_type):
    """
    Predict credit score and default probability
    """
    # Base score calculation
    base_score = 650
    
    # Age factor
    if age < 25:
        base_score -= 20
    elif 25 <= age <= 35:
        base_score += 30
    elif 36 <= age <= 50:
        base_score += 40
    elif age > 50:
        base_score += 25
    else:
        base_score += 20
    
    # Income factor (in lakhs)
    income_lakhs = income / 100000
    if income_lakhs > 20:
        base_score += 50
    elif income_lakhs > 10:
        base_score += 30
    elif income_lakhs > 5:
        base_score += 15
    else:
        base_score += 5
    
    # Loan-to-income penalty
    lti_ratio = (loan_amount / income * 100) if income > 0 else 0
    if lti_ratio > 50:
        base_score -= 40
    elif lti_ratio > 30:
        base_score -= 20
    elif lti_ratio > 20:
        base_score -= 10
    elif lti_ratio < 10:
        base_score += 10
    
    # Credit utilization penalty
    if credit_utilization_ratio > 80:
        base_score -= 40
    elif credit_utilization_ratio > 60:
        base_score -= 30
    elif credit_utilization_ratio > 40:
        base_score -= 15
    elif credit_utilization_ratio < 20:
        base_score += 15
    elif credit_utilization_ratio < 30:
        base_score += 10
    
    # Delinquency penalty
    if delinquency_ratio > 30:
        base_score -= 40
    elif delinquency_ratio > 20:
        base_score -= 25
    elif delinquency_ratio > 10:
        base_score -= 15
    elif delinquency_ratio > 5:
        base_score -= 5
    
    # DPD penalty
    if avg_dpd_per_delinquency > 90:
        base_score -= 40
    elif avg_dpd_per_delinquency > 60:
        base_score -= 30
    elif avg_dpd_per_delinquency > 30:
        base_score -= 15
    elif avg_dpd_per_delinquency > 7:
        base_score -= 5
    
    # Number of accounts
    if num_open_accounts > 10:
        base_score -= 10
    elif num_open_accounts > 5:
        base_score -= 5
    elif num_open_accounts > 0:
        base_score += 5
    
    # Residence bonus
    if residence_type == "Owned":
        base_score += 30
    elif residence_type == "Mortgage":
        base_score += 15
    elif residence_type == "Rented":
        base_score += 5
    else:  # With Family
        base_score += 0
    
    # Loan purpose adjustment
    if loan_purpose == "Home":
        base_score += 25
    elif loan_purpose == "Education":
        base_score += 20
    elif loan_purpose == "Personal":
        base_score += 10
    
    # Loan type adjustment
    if loan_type == "Secured":
        base_score += 15
    elif loan_type == "Unsecured":
        base_score -= 10
    
    # Ensure score is within range
    credit_score = max(300, min(int(base_score), 850))
    
    # Calculate default probability
    # Higher score = lower probability
    score_ratio = (850 - credit_score) / 550  # 0 to 1
    default_probability = max(0.01, min(0.99, score_ratio * 0.8))
    
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
