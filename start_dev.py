#!/usr/bin/env python3
"""
Development startup script for YouTube Notes Generator
This script helps start both frontend and backend servers
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python
    try:
        subprocess.run([sys.executable, "--version"], check=True, capture_output=True)
        print("✅ Python is installed")
    except subprocess.CalledProcessError:
        print("❌ Python is not installed or not in PATH")
        return False
    
    # Check Node.js
    try:
        subprocess.run(["node", "--version"], check=True, capture_output=True)
        print("✅ Node.js is installed")
    except subprocess.CalledProcessError:
        print("❌ Node.js is not installed or not in PATH")
        return False
    
    # Check npm
    try:
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
        print("✅ npm is installed")
    except subprocess.CalledProcessError:
        print("❌ npm is not installed or not in PATH")
        return False
    
    return True

def install_backend_dependencies():
    """Install Python dependencies for backend"""
    print("📦 Installing backend dependencies...")
    backend_dir = Path("backend")
    
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", 
            str(backend_dir / "requirements.txt")
        ], check=True)
        print("✅ Backend dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install backend dependencies")
        return False

def install_frontend_dependencies():
    """Install Node.js dependencies for frontend"""
    print("📦 Installing frontend dependencies...")
    frontend_dir = Path("frontend")
    
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    try:
        subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
        print("✅ Frontend dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install frontend dependencies")
        return False

def check_env_file():
    """Check if .env file exists in backend"""
    backend_dir = Path("backend")
    env_file = backend_dir / ".env"
    
    if not env_file.exists():
        print("⚠️  No .env file found in backend directory")
        print("📝 Please create a .env file with your OpenRouter API key:")
        print("   OPENROUTER_API_KEY=your_api_key_here")
        print("   Get your API key from: https://openrouter.ai/")
        return False
    
    print("✅ .env file found")
    return True

def main():
    print("🚀 YouTube Notes Generator - Development Setup")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies and try again")
        sys.exit(1)
    
    # Install dependencies
    if not install_backend_dependencies():
        print("\n❌ Failed to install backend dependencies")
        sys.exit(1)
    
    if not install_frontend_dependencies():
        print("\n❌ Failed to install frontend dependencies")
        sys.exit(1)
    
    # Check environment file
    check_env_file()
    
    print("\n✅ Setup complete!")
    print("\n📋 To start the application:")
    print("1. Start the backend: cd backend && python run.py")
    print("2. Start the frontend: cd frontend && npm run dev")
    print("\n🌐 The application will be available at:")
    print("   Frontend: http://localhost:5173")
    print("   Backend API: http://localhost:8000")
    print("   API Docs: http://localhost:8000/docs")

if __name__ == "__main__":
    main() 