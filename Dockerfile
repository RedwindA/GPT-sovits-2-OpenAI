# Use the official Python image
FROM python:3.10-slim

# Install ffmpeg and any other dependencies
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app.py /app/

# Expose the port that the app runs on
EXPOSE 5000

# Set the command to run the application
CMD ["python", "app.py"]