# Base image: Python 3.9 slim version
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install required dependencies
# Flask = web framework, pytz = timezone support
RUN pip install Flask pytz

# Copy the application code into the container
COPY app.py .

# Expose port 5000 to allow external access
EXPOSE 5000

# Command to run the application when the container starts
CMD ["python", "app.py"]
