# prediction_helper.py - NO EXTERNAL DEPENDENCIES
import numpy as np


def predict(age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
            delinquency_ratio, credit_utilization_ratio, num_open_accounts,
            residence_type, loan_purpose, loan_type):
    """Simple credit score calculator"""

    # Base calculation
    base_score = 650

    # Age factor
    if 30 <= age <= 50:
        base_score += 30
    elif age < 30:
        base_score += 20 - (30 - age)
    else:
        base_score += 30 - (age - 50)

    # Income factor (in lakhs)
    income_lakhs = income / 100000
    base_score += min(income_lakhs * 5, 50)

    # Loan-to-income penalty
    lti = loan_amount / income if income > 0 else 0
    if lti > 3:
        base_score -= 40
    elif lti > 2:
        base_score -= 20

    # Credit utilization penalty
    if credit_utilization_ratio > 50:
        base_score -= 30
    elif credit_utilization_ratio > 30:
        base_score -= 15
    elif credit_utilization_ratio < 20:
        base_score += 15

    # Delinquency penalty
    if delinquency_ratio > 20:
        base_score -= 40
    elif delinquency_ratio > 10:
        base_score -= 20

    # DPD penalty
    if avg_dpd_per_delinquency > 30:
        base_score -= 25
    elif avg_dpd_per_delinquency > 7:
        base_score -= 10

    # Residence bonus
    if residence_type == "Owned":
        base_score += 20
    elif residence_type == "Mortgage":
        base_score += 10

    # Loan purpose bonus
    if loan_purpose == "Home":
        base_score += 20
    elif loan_purpose == "Education":
        base_score += 15

    # Final score
    credit_score = max(300, min(round(base_score), 850))

    # Default probability (inverse of score)
    default_probability = max(0.01, min(0.99, (850 - credit_score) / 550 * 0.8))

    # Rating
    if credit_score >= 750:
        rating = "Excellent"
    elif credit_score >= 650:
        rating = "Good"
    elif credit_score >= 550:
        rating = "Fair"
    else:
        rating = "Poor"

    return default_probability, credit_score, rating