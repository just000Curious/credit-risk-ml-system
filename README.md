# 🏦 Credit Risk Modeling & Prediction System

## 📋 Overview
An AI-powered system that predicts loan default probability with 92.4% accuracy. Designed for financial institutions to make data-driven lending decisions through an intuitive web interface.

## 🎯 What It Does
**Input Client Data** → **AI Analysis** → **Risk Assessment** → **Actionable Recommendations**

### Core Functionality:
- 📊 **Real-time Risk Scoring**: Calculates default probability instantly
- 🎯 **Credit Score Generation**: Produces 300-850 credit scores
- 💡 **Decision Support**: Clear approve/conditional/decline recommendations
- 🔄 **Scenario Planning**: "What-if" analysis for credit improvement

## 📸 Visual Preview

### Dashboard Overview
<img width="1914" height="792" alt="Dashboard Overview" src="https://github.com/user-attachments/assets/4940e95a-60e2-4720-9e35-6584a37e02d8" />

### Input Sections
<img width="1769" height="221" alt="Input Form" src="https://github.com/user-attachments/assets/b5658eab-b70c-498b-ace1-02afc9e22b66" />

### Risk Analysis Results
<img width="1755" height="475" alt="Risk Analysis" src="https://github.com/user-attachments/assets/adfce167-569a-4336-b1ae-d8810cf02c96" />

### Credit Score Display
<img width="1755" height="454" alt="Credit Score" src="https://github.com/user-attachments/assets/d9583c2d-fd1f-402a-996d-1ed950da803b" />

### Financial Metrics
<img width="1717" height="203" alt="Financial Metrics" src="https://github.com/user-attachments/assets/b14e5a20-eb54-48c2-8e7b-7f70607efa3d" />

### Advisor Recommendations
<img width="1797" height="579" alt="Advisor Notes" src="https://github.com/user-attachments/assets/ea662f6d-6159-491b-b703-9872f7a0cbcd" />

### Scenario Planning Tools
<img width="1783" height="517" alt="Scenario Planning" src="https://github.com/user-attachments/assets/3263b42c-3409-4c77-9d18-d40d6c6b45d0" />

## 🚀 Quick Start

### 1. Install Dependencies
```bash
git clone [repository-url]
cd credit-risk-ml-system/app
pip install -r requirements.txt
```

### 2. Run Application
```bash
streamlit run main.py
```

### 3. Access Dashboard
Open browser: `http://localhost:8501`

## 📝 How to Use

### Step 1: Enter Client Information
- **Personal Details**: Age, Residence, Employment
- **Financial Info**: Income, Loan Amount, Tenure
- **Credit History**: Utilization, Delinquency, Payments

### Step 2: Generate Assessment
Click **"GENERATE COMPREHENSIVE CREDIT ASSESSMENT"**

### Step 3: Review Results
Dashboard shows:
- ✅ Credit Score (300-850)
- 📉 Default Probability
- 📊 Financial Ratios
- 🎯 Advisor Recommendations
- 🔄 Scenario Planning

## 📊 Model Performance
- **Accuracy**: 92.4%
- **Training Data**: 58,421 samples
- **Response Time**: < 2 seconds
- **Features**: 12 key risk factors

## 🎨 Dashboard Features

### Visual Components:
1. **Score Spotlight** - Animated credit score display
2. **Risk Meter** - Visual probability indicator
3. **Financial Metrics** - Color-coded ratio cards
4. **Radar Chart** - Multi-factor risk analysis
5. **Advisor Notes** - Customized recommendations
6. **Scenario Planner** - Interactive "what-if" tools

### Client Tiers:
- **💎 Tier-1 Elite** (750+) - Premium treatment
- **⭐ Tier-2 Standard** (650-749) - Standard processing
- **📝 Tier-3 Developing** (<650) - Guidance program

## 💼 Who Should Use This

### Primary Users:
- Bank Relationship Managers
- Credit Analysts
- Financial Advisors
- FinTech Platforms

### Applications:
- Personal Loans & Mortgages
- Small Business Lending
- Credit Portfolio Management
- Financial Education

## 📈 Key Metrics

### Default Probability:
- Low Risk (<10%)
- Moderate Risk (10-25%)
- High Risk (>25%)

### Credit Score:
- Poor (300-579)
- Fair (580-649)
- Good (650-749)
- Excellent (750+)

### Financial Ratios:
- Loan-to-Income (LTI)
- Debt-to-Income (DTI)
- Monthly EMI Calculation

## 📁 Project Structure
```
credit-risk-ml-system/
├── app/                    # Web application
├── artifacts/             # Trained ML models
├── dataset/              # Training data
└── notebook/            # Model development
```

## 🔧 Technical Stack
- **Frontend**: Streamlit with custom CSS
- **ML Model**: XGBoost (92.4% accuracy)
- **Visualization**: Plotly charts
- **Backend**: Python with scikit-learn

## 🎯 Business Benefits

### For Advisors:
- Quick risk assessment
- Professional client presentations
- Data-driven decisions
- Client education tool

### For Institutions:
- Consistent risk evaluation
- Reduced processing time
- Improved portfolio quality
- Compliance support

## 📦 Deployment

### Simple Setup:
```bash
# Local deployment
streamlit run main.py
```

### Production Options:
- Docker container
- Cloud hosting (AWS/Azure)
- On-premise servers

## 🆘 Getting Started

### Prerequisites:
- Python 3.8+
- 4GB RAM
- Modern web browser
- Git installed

### Quick Test:
1. Clone repository
2. Install dependencies
3. Run application
4. Open browser to localhost:8501
5. Enter test data

### Sample Test Data:
```
Age: 35
Income: ₹1,200,000
Loan: ₹5,000,000
Utilization: 35%
Delinquency: 10%
```

---

## 🏆 Why Choose This System

### Key Advantages:
1. **92.4% Accuracy** - Validated model performance
2. **Real-time Analysis** - Results in under 2 seconds
3. **No Technical Skills Required** - User-friendly interface
4. **Professional Reports** - Client-ready visualizations
5. **Flexible** - Works for all loan types

### Business Impact:
- Reduce bad loans
- Improve client satisfaction
- Accelerate processing
- Enhance risk management

---

## 🎯 In One Sentence
**An AI-powered dashboard that transforms complex credit risk analysis into simple, actionable insights for financial professionals.**

---

*Ready to start? Clone and run `streamlit run main.py`*
