#!/usr/bin/env bash
# Build script for Render deployment

# Install dependencies
pip install -r requirements.txt

# Create temp directory if it doesn't exist
mkdir -p temp

# Set permissions
chmod +x run.py 