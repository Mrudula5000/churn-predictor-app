import streamlit as st
import requests
import os

# Configure application backend URL context 
# Uses localhost for local execution or dynamic environment variable URLs in production cloud configurations
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(page_title="Customer Churn Intelligence Portal", layout="centered")
st.title("📊 Customer Churn Predictor Engine")
st.write("Determine the likelihood of a client terminating service operations instantly.")

# Create structured input fields 
with st.form("prediction_form"):
    st.subheader("Customer Metrics Profile")
    tenure = st.number_input("Tenure (Months)", min_value=0, max_value=120, value=12)
    monthly_charges = st.number_input("Monthly Charges ($)", min_value=0.0, value=45.50)
    total_charges = st.number_input("Total Charges ($)", min_value=0.0, value=546.00)
    customer_support_calls = st.number_input("Customer Support Interactions", min_value=0, max_value=20, value=1)
    
    submit_button = st.form_submit_button(label="Compute Churn Risks")

if submit_button:
    payload = {
        "tenure": int(tenure),
        "monthly_charges": float(monthly_charges),
        "total_charges": float(total_charges),
        "customer_support_calls": int(customer_support_calls)
    }
    
    with st.spinner("Processing local calculations with engine API..."):
        try:
            # Phase 3 Integration: POST request execution to the API
            response = requests.post(f"{BACKEND_URL}/predict", json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                probability = result["churn_probability"] * 100
                
                st.write("---")
                if result["churn_prediction"] == 1:
                    st.error(f"⚠️ **High Churn Risk Detected!** Probability: {probability:.2f}%")
                else:
                    st.success(f"✅ **Low Churn Risk / Safe Profile.** Probability: {probability:.2f}%")
            else:
                st.error(f"Backend API threw an error: {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("Error: Could not reach the backend API server. Is it running?")
