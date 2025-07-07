#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install system dependencies for Pillow
apt-get update
apt-get install -y --no-install-recommends \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    zlib1g-dev \
    libopenjp2-7-dev

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install Pillow separately with binary option
pip install --only-binary :all: pillow==10.1.0

# Create necessary directories
mkdir -p uploads/prescriptions
mkdir -p uploads/delivery_proofs
mkdir -p uploads/medicines

# Make the script executable
chmod +x build.sh 