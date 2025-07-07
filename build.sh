#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install Python dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p uploads/prescriptions
mkdir -p uploads/delivery_proofs
mkdir -p uploads/medicines

# Make the script executable
chmod +x build.sh 