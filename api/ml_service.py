import os
import joblib
import numpy as np
import pandas as pd
from pydantic import BaseModel

# Determine path to the model artifact
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'app', 'artifacts', 'model_data.joblib')

try:
    model_data = joblib.load(MODEL_PATH)
    model = model_data['model']
    scaler = model_data['scaler']
    features = model_data['features']
    cols_to_scale = model_data['cols_to_scale']
except Exception as e:
    print(f"Warning: Could not load model from {MODEL_PATH}. Error: {e}")
    model = None


def calculate_credit_score(input_df, base_score=300, scale_length=600):
    if model is None:
        return 0.5, 600, "Average"

    x = np.dot(input_df.values, model.coef_.T) + model.intercept_
    default_probability = 1 / (1 + np.exp(-x))
    non_default_probability = 1 - default_probability
    credit_score = base_score + non_default_probability.flatten() * scale_length

    def get_rating(score):
        if 300 <= score < 500:
            return 'Poor'
        elif 500 <= score < 650:
            return 'Average'
        elif 650 <= score < 750:
            return 'Good'
        elif 750 <= score <= 900:
            return 'Excellent'
        return 'Undefined'

    rating = get_rating(credit_score[0])
    return float(default_probability.flatten()[0]), int(credit_score[0]), rating


def predict_risk(data):
    """Takes a PredictionRequest object and returns probability, score, and rating."""
    input_data = {
        'age': data.age,
        'loan_tenure_months': data.loan_tenure_months,
        'number_of_open_accounts': data.num_open_accounts,
        'credit_utilization_ratio': data.credit_utilization_ratio,
        'loan_to_income': data.loan_amount / data.annual_income if data.annual_income > 0 else 0,
        'delinquency_ratio': data.delinquency_ratio,
        'avg_dpd_per_delinquency': data.avg_dpd_per_delinquency,
        'residence_type_Owned': 1 if data.residence_type == 'Owned' else 0,
        'residence_type_Rented': 1 if data.residence_type == 'Rented' else 0,
        'loan_purpose_Education': 1 if data.loan_purpose == 'Education' else 0,
        'loan_purpose_Home': 1 if data.loan_purpose == 'Home' else 0,
        'loan_purpose_Personal': 1 if data.loan_purpose == 'Personal' else 0,
        'loan_type_Unsecured': 1 if data.loan_type == 'Unsecured' else 0,
        'number_of_dependants': 1,
        'years_at_current_address': 1,
        'zipcode': 1,
        'sanction_amount': 1,
        'processing_fee': 1,
        'gst': 1,
        'net_disbursement': 1,
        'principal_outstanding': 1,
        'bank_balance_at_application': 1,
        'number_of_closed_accounts': 1,
        'enquiry_count': 1
    }

    df = pd.DataFrame([input_data])
    if model is not None:
        df[cols_to_scale] = scaler.transform(df[cols_to_scale])
        df = df[features]
        return calculate_credit_score(df)
    
    return 0.5, 600, "Average"
