# Use Python 3.10 slim image
FROM python:3.10-slim

# Avoid prompts and upgrade system
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies required by mediapipe, opencv, etc.
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1 \
    libglib2.0-0 \
    libgtk2.0-dev \
    libgtk-3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the port your app runs on (Flask default is 5000)
EXPOSE 5000

# Run using gunicorn (recommended for production)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]