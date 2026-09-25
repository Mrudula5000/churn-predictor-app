import os
import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# 1. Create a directory for artifacts
os.makedirs("model", exist_ok=True)

# 2. Simulate training data (Features: tenure, monthly_charges, total_charges)
X_train = np.array([[1, 20.0, 20.0], [12, 50.0, 600.0], [24, 80.0, 1920.0], [72, 110.0, 7920.0]])
y_train = np.array([1, 1, 0, 0]) # 1 = Churn, 0 = Stay

# 3. Bundle Preprocessor and Model into a Pipeline to avoid "The Trap"
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression())
])

# 4. Train the integrated architecture
pipeline.fit(X_train, y_train)

# 5. Serialize and freeze the state
joblib.dump(pipeline, "model/churn_pipeline.pkl")
print("Model and Preprocessor successfully packaged into 'model/churn_pipeline.pkl'")
