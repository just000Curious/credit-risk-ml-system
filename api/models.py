from pydantic import BaseModel, Field

class PredictionRequest(BaseModel):
    age: int = Field(..., ge=18, le=100, description="Age of the applicant")
    annual_income: float = Field(..., ge=0, description="Gross annual income in INR")
    loan_amount: float = Field(..., gt=0, description="Requested loan amount in INR")
    loan_tenure_months: int = Field(..., gt=0, description="Loan duration in months")
    avg_dpd_per_delinquency: float = Field(..., ge=0, description="Average days past due per delinquency")
    delinquency_ratio: float = Field(..., ge=0, le=100, description="Percentage of delinquent accounts")
    credit_utilization_ratio: float = Field(..., ge=0, le=100, description="Percentage of available credit used")
    num_open_accounts: int = Field(default=2, ge=0, description="Number of open credit accounts")
    residence_type: str = Field(..., description="Type of residence (e.g., 'Owned', 'Rented')")
    loan_purpose: str = Field(default="Home", description="Purpose of the loan")
    loan_type: str = Field(default="Secured", description="Type of the loan")

class PredictionResponse(BaseModel):
    probability: float = Field(..., description="Probability of default (0.0 to 1.0)")
    credit_score: int = Field(..., description="Calculated credit score (300 to 900)")
    rating: str = Field(..., description="Risk rating category (e.g., 'Excellent', 'Poor')")
    loan_to_income_ratio: float = Field(..., description="Calculated Loan-to-Income ratio (%)")
    debt_to_income_ratio: float = Field(..., description="Calculated Debt-to-Income ratio (%)")
    monthly_emi: float = Field(..., description="Estimated monthly EMI")
