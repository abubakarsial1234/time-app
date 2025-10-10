# Base image: Python 3.9 slim version
FROM public.ecr.aws/docker/library/python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY app.py .

# Set timezone
ENV TZ=UTC

# Expose port 5000 to allow external access
EXPOSE 5000

# Command to run the application when the container starts
CMD ["python", "app.py"]
