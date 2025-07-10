#!/usr/bin/env python3
"""
Configuration settings for YouTube Notes Generator
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # API Keys
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    
    # API Settings
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "mistralai/mistral-small-3.2-24b-instruct:free")
    
    # Request limits
    MAX_TRANSCRIPT_LENGTH = 8000  # characters
    MAX_TOKENS = 2000
    TEMPERATURE = 0.7
    TOP_P = 0.9
    
    # PDF Settings
    PDF_PAGE_SIZE = "A4"
    PDF_MARGIN = 1  # inch
    
    # CORS Settings
    ALLOWED_ORIGINS = ["*"]  # In production, specify your frontend URL
    
    # File Settings
    TEMP_DIR = "temp"
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    # Timeout Settings
    REQUEST_TIMEOUT = 60.0  # seconds
    API_TIMEOUT = 30.0  # seconds 