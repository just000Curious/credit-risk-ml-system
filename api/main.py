from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.models import PredictionRequest, PredictionResponse
from api.ml_service import predict_risk

app = FastAPI(
    title="EliteCredit API",
    description="Backend API for Credit Risk Modelling",
    version="1.0.0"
)

# Enable CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the exact frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "EliteCredit API is running"}

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/predict", response_model=PredictionResponse)
def predict_credit_risk(request: PredictionRequest):
    try:
        probability, credit_score, rating = predict_risk(request)
        
        # Calculate ratios
        loan_to_income = (request.loan_amount / request.annual_income * 100) if request.annual_income > 0 else 0
        monthly_emi = request.loan_amount / request.loan_tenure_months if request.loan_tenure_months > 0 else 0
        debt_to_income = (monthly_emi * 12 / request.annual_income * 100) if request.annual_income > 0 else 0
        
        return PredictionResponse(
            probability=probability,
            credit_score=credit_score,
            rating=rating,
            loan_to_income_ratio=loan_to_income,
            debt_to_income_ratio=debt_to_income,
            monthly_emi=monthly_emi
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
