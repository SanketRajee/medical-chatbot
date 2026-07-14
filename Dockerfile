# Use an official Python runtime as a parent image (slim version for a smaller footprint)
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
# 1. Install CPU-only PyTorch first (default PyTorch is ~2.5GB with CUDA and crashes Docker builds)
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# 2. Install the rest of the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose port 5000 for FastAPI
EXPOSE 5000

# Run the FastAPI server using Uvicorn
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
