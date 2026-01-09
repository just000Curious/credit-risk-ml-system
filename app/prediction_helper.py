# prediction_helper.py - Self-contained with original logic
import numpy as np
import pandas as pd

# Create a simple model simulation without joblib/scikit-learn
class SimpleModel:
    def __init__(self):
        # Simulated coefficients based on your original model structure
        self.coef_ = np.array([[
            -0.05,  # age
            -0.002, # loan_tenure_months  
            0.01,   # number_of_open_accounts
            0.03,   # credit_utilization_ratio
            0.02,   # loan_to_income
            0.04,   # delinquency_ratio
            0.005,  # avg_dpd_per_delinquency
            -0.2,   # residence_type_Owned
            0.1,    # residence_type_Rented
            -0.15,  # loan_purpose_Education
            -0.3,   # loan_purpose_Home
            0.2,    # loan_purpose_Personal
            0.25,   # loan_type_Unsecured
            # Dummy coefficients for remaining features
            -0.001, 0.001, 0.0001, -0.0002, 0.0003, 
            0.0001, -0.0002, 0.001, 0.0005, 0.0003,
            0.0002
        ]])
        self.intercept_ = np.array([0.3])

class SimpleScaler:
    def __init__(self):
        self.min_ = None
        self.scale_ = None
    
    def fit(self, X):
        self.min_ = np.min(X, axis=0)
        self.scale_ = np.max(X, axis=0) - self.min_
        self.scale_[self.scale_ == 0] = 1
        return self
    
    def transform(self, X):
        return (X - self.min_) / self.scale_

# Initialize model components
features = [
    'age', 'loan_tenure_months', 'number_of_open_accounts', 
    'credit_utilization_ratio', 'loan_to_income', 'delinquency_ratio',
    'avg_dpd_per_delinquency', 'residence_type_Owned', 'residence_type_Rented',
    'loan_purpose_Education', 'loan_purpose_Home', 'loan_purpose_Personal',
    'loan_type_Unsecured', 'number_of_dependants', 'years_at_current_address',
    'zipcode', 'sanction_amount', 'processing_fee', 'gst', 'net_disbursement',
    'principal_outstanding', 'bank_balance_at_application', 
    'number_of_closed_accounts', 'enquiry_count'
]

cols_to_scale = [
    'age', 'loan_tenure_months', 'number_of_open_accounts', 
    'credit_utilization_ratio', 'loan_to_income', 'delinquency_ratio',
    'avg_dpd_per_delinquency', 'number_of_dependants', 
    'years_at_current_address', 'zipcode', 'sanction_amount', 
    'processing_fee', 'gst', 'net_disbursement', 
    'principal_outstanding', 'bank_balance_at_application', 
    'number_of_closed_accounts', 'enquiry_count'
]

# Create and fit scaler with reasonable ranges
scaler = SimpleScaler()
np.random.seed(42)

# Generate realistic training data for scaler
dummy_data = []
for _ in range(100):
    row = [
        np.random.randint(20, 70),  # age
        np.random.randint(12, 360),  # loan_tenure_months
        np.random.randint(1, 15),   # number_of_open_accounts
        np.random.uniform(0, 100),  # credit_utilization_ratio
        np.random.uniform(0.5, 5),  # loan_to_income
        np.random.uniform(0, 50),   # delinquency_ratio
        np.random.uniform(0, 90),   # avg_dpd_per_delinquency
        np.random.randint(1, 5),    # number_of_dependants
        np.random.randint(1, 20),   # years_at_current_address
        np.random.randint(100000, 999999),  # zipcode
        np.random.uniform(100000, 10000000),  # sanction_amount
        np.random.uniform(1000, 50000),  # processing_fee
        np.random.uniform(100, 10000),   # gst
        np.random.uniform(90000, 9000000),  # net_disbursement
        np.random.uniform(50000, 8000000),  # principal_outstanding
        np.random.uniform(10000, 500000),   # bank_balance_at_application
        np.random.randint(0, 10),   # number_of_closed_accounts
        np.random.randint(0, 10)    # enquiry_count
    ]
    dummy_data.append(row)

scaler.fit(np.array(dummy_data))

# Initialize model
model = SimpleModel()

def prepare_input(age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
                  delinquency_ratio, credit_utilization_ratio, num_open_accounts, residence_type,
                  loan_purpose, loan_type):
    # Calculate loan_to_income
    loan_to_income = loan_amount / income if income > 0 else 0
    
    # Create input dictionary
    input_data = {
        'age': float(age),
        'loan_tenure_months': float(loan_tenure_months),
        'number_of_open_accounts': float(num_open_accounts),
        'credit_utilization_ratio': float(credit_utilization_ratio),
        'loan_to_income': float(loan_to_income),
        'delinquency_ratio': float(delinquency_ratio),
        'avg_dpd_per_delinquency': float(avg_dpd_per_delinquency),
        'residence_type_Owned': 1.0 if residence_type == 'Owned' else 0.0,
        'residence_type_Rented': 1.0 if residence_type == 'Rented' else 0.0,
        'loan_purpose_Education': 1.0 if loan_purpose == 'Education' else 0.0,
        'loan_purpose_Home': 1.0 if loan_purpose == 'Home' else 0.0,
        'loan_purpose_Personal': 1.0 if loan_purpose == 'Personal' else 0.0,
        'loan_type_Unsecured': 1.0 if loan_type == 'Unsecured' else 0.0,
        'number_of_dependants': 2.0,
        'years_at_current_address': 5.0,
        'zipcode': 560001.0,
        'sanction_amount': float(loan_amount),
        'processing_fee': float(loan_amount * 0.01),
        'gst': float(loan_amount * 0.01 * 0.18),
        'net_disbursement': float(loan_amount * 0.99),
        'principal_outstanding': float(loan_amount),
        'bank_balance_at_application': float(income / 12),
        'number_of_closed_accounts': 2.0,
        'enquiry_count': 1.0
    }
    
    # Create DataFrame
    df = pd.DataFrame([input_data])
    
    # Scale columns
    df_scaled = df.copy()
    df_scaled[cols_to_scale] = scaler.transform(df[cols_to_scale])
    
    # Ensure all features are present
    for feature in features:
        if feature not in df_scaled.columns:
            df_scaled[feature] = 0.0
    
    return df_scaled[features]

def calculate_credit_score(input_df, base_score=300, scale_length=600):
    x = np.dot(input_df.values, model.coef_.T) + model.intercept_
    
    # Sigmoid function
    default_probability = 1 / (1 + np.exp(-x))
    
    non_default_probability = 1 - default_probability
    credit_score = base_score + non_default_probability.flatten() * scale_length
    
    # Clamp score
    credit_score = np.clip(credit_score, 300, 900)
    
    # Rating
    def get_rating(score):
        score = float(score)
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

def predict(age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
            delinquency_ratio, credit_utilization_ratio, num_open_accounts,
            residence_type, loan_purpose, loan_type):
    # Prepare input
    input_df = prepare_input(age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
                             delinquency_ratio, credit_utilization_ratio, num_open_accounts, 
                             residence_type, loan_purpose, loan_type)
    
    # Calculate score
    probability, credit_score, rating = calculate_credit_score(input_df)
    
    return probability, credit_score, rating

# Test
if __name__ == "__main__":
    prob, score, rating = predict(
        age=35,
        income=1200000,
        loan_amount=5000000,
        loan_tenure_months=36,
        avg_dpd_per_delinquency=5,
        delinquency_ratio=10,
        credit_utilization_ratio=35,
        num_open_accounts=2,
        residence_type="Owned",
        loan_purpose="Home",
        loan_type="Unsecured"
    )
    print(f"Probability: {prob:.2%}")
    print(f"Score: {score}")
    print(f"Rating: {rating}")
