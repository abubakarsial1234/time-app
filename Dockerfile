# --- CHANGE: AWS ki bajaye Google Mirror use karein ---
FROM mirror.gcr.io/library/python:3.11-slim

# Baki saara code bilkul sahi hai, isay wese hi rehne dein
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y tzdata && rm -rf /var/lib/apt/lists/*

# Requirements copy karein
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code copy karein
COPY app.py .

# Port 80 expose karein
EXPOSE 80

# App start karein
CMD ["python", "app.py"]
