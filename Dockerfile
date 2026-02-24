# Base image
FROM public.ecr.aws/docker/library/python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y tzdata && rm -rf /var/lib/apt/lists/*

# Requirements copy karein
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code copy karein
COPY app.py .

# ECS ke liye Port 80 expose karein (Match with CDK)
EXPOSE 80

# App start karein
CMD ["python", "app.py"]
