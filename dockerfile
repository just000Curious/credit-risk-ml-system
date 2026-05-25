# Backend Dockerfile for EliteCredit Credit Risk API

FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project (so api/ and app/ are both available)
COPY . .

EXPOSE 8000

# Use 0.0.0.0 to accept connections from outside the container
# Remove --reload in production
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
