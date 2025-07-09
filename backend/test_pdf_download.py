#!/usr/bin/env python3
"""
Simple PDF download test
"""

import requests
import json

def test_pdf_download():
    """Test PDF download functionality"""
    
    print("🧪 Testing PDF Download...")
    print("=" * 50)
    
    # Sample notes
    sample_notes = """# 📋 Overview & Summary

This video covers the fundamentals of machine learning.

## 🎯 Key Concepts
- Machine Learning basics
- AI fundamentals
- Data science principles

## 📚 Detailed Explanations
Machine learning is a subset of artificial intelligence."""

    # Test data
    data = {
        "notes": sample_notes,
        "title": "Test Notes",
        "youtube_url": "https://www.youtube.com/watch?v=test",
        "metadata": {
            "video_author": "Test Author",
            "video_duration": "10:00",
            "publish_date": "2024-01-01",
            "view_count": "1000"
        }
    }
    
    try:
        print("📝 Step 1: Testing PDF generation...")
        response = requests.post(
            "http://localhost:8000/generate-pdf",
            json=data,
            timeout=60
        )
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📄 Content-Type: {response.headers.get('content-type', 'Unknown')}")
        print(f"📏 Content-Length: {response.headers.get('content-length', 'Unknown')}")
        
        if response.status_code == 200:
            print("✅ PDF Generated Successfully!")
            print(f"📏 Size: {len(response.content)} bytes")
            
            # Save PDF
            filename = "test_download.pdf"
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"💾 PDF saved as: {filename}")
            
            # Check if file exists and has content
            import os
            if os.path.exists(filename):
                file_size = os.path.getsize(filename)
                print(f"📁 File exists, size: {file_size} bytes")
                if file_size > 0:
                    print("✅ File download successful!")
                else:
                    print("❌ File is empty!")
            else:
                print("❌ File was not created!")
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Server is not running")
        print("Please start the server with: uvicorn main:app --reload")
    except requests.exceptions.Timeout:
        print("❌ Timeout Error: Request took too long")
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_health():
    """Test server health"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running")
            return True
        else:
            print(f"❌ Server health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        return False

if __name__ == "__main__":
    print("🚀 PDF Download Test")
    print("=" * 60)
    
    if test_health():
        test_pdf_download()
    else:
        print("\n❌ Please start the server first:")
        print("   cd backend")
        print("   uvicorn main:app --reload") 