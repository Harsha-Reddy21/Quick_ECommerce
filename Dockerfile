FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    zlib1g-dev \
    libopenjp2-7-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir --only-binary :all: pillow==10.1.0

# Copy the rest of the application
COPY . .

# Create necessary directories
RUN mkdir -p uploads/prescriptions uploads/delivery_proofs uploads/medicines

# Expose the port the app will run on
EXPOSE 10000

# Command to run the application
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-10000} 