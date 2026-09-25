import os
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Initialize the FastAPI Application Engine
app = FastAPI(title="Customer Churn Prediction API")

# Resolve model path dynamically relative to the application structure
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, "..", "model", "churn_pipeline.pkl")
    model_pipeline = joblib.load(MODEL_PATH)
except Exception as e:
    model_pipeline = None
    print(f"Warning: Model payload not loaded yet. Error: {e}")

# Define Pydantic Input Schema for Data Validation
class CustomerData(BaseModel):
    tenure: int
    MonthlyCharges: float
    TotalCharges: float
    Gender_Male: int
    Contract_One_year: int
    Contract_Two_year: int
    InternetService_Fiber_optic: int
    InternetService_No: int
    PaymentMethod_Credit_card_automatic: int
    PaymentMethod_Electronic_check: int
    PaymentMethod_Mailed_check: int

@app.get("/health")
def health_check():
    """Sanity check endpoint for infrastructure tracking."""
    if model_pipeline is None:
        return {"status": "unhealthy", "model_loaded": False}
    return {"status": "healthy", "model_loaded": True}

@app.post("/predict")
def predict_churn(data: CustomerData):
    """Core predictive endpoint running inference on incoming payloads."""
    if model_pipeline is None:
        raise HTTPException(status_code=503, detail="Machine Learning Model Payload not loaded.")
    
    try:
        # Structure incoming values into model parameters
        input_data = [[
            data.tenure, data.MonthlyCharges, data.TotalCharges, data.Gender_Male,
            data.Contract_One_year, data.Contract_Two_year, data.InternetService_Fiber_optic,
            data.InternetService_No, data.PaymentMethod_Credit_card_automatic,
            data.PaymentMethod_Electronic_check, data.PaymentMethod_Mailed_check
        ]]
        
        # Execute predictions and capture probability scores
        prediction = int(model_pipeline.predict(input_data)[0])
        probability = float(model_pipeline.predict_proba(input_data)[0][1])
        
        return {
            "prediction": prediction,
            "probability": round(probability * 100, 2),
            "risk_status": "High" if probability >= 0.5 else "Low"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction Pipeline Crash: {e}")
