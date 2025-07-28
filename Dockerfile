# FROM python:3.10
# WORKDIR /app
# COPY . .
# RUN pip install -r requirements.txt
# CMD ["python", "app/main.py"]

# Use Python base image for amd64 architecture
FROM --platform=linux/amd64 python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY app/ ./app/
COPY input/ ./input/
COPY output/ ./output/

# Set environment variables (optional, but good for UTF-8 support)
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8

# Run the app
CMD ["python", "app/main.py"]
