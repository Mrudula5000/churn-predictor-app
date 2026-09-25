# Step 1: Use an official lightweight Python image
FROM python:3.10-slim

# Step 2: Establish the working directory inside the container
WORKDIR /workspace

# Step 3: Copy only the requirement manifest first
COPY requirements.txt .

# Step 4: Execute package installations
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Transfer all local project files cleanly
COPY . .

# Step 6: Expose dedicated application system network ports
EXPOSE 8000
EXPOSE 8501

# Step 7: Launch both microservice layers concurrently
CMD python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend.py --server.port 8501 --server.address 0.0.0.0
