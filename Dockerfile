# Use official Python image as a base
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI app
COPY ./app /app

# Expose FastAPI server port (default 8000)
EXPOSE 8001