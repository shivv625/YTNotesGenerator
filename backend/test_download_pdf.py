#!/usr/bin/env python3
"""
Test the download-pdf endpoint
"""

import requests
import json

def test_download_pdf():
    """Test the download-pdf endpoint"""
    
    print("🧪 Testing /download-pdf endpoint...")
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
        "title": "Download Test Notes",
        "youtube_url": "https://www.youtube.com/watch?v=test",
        "metadata": {
            "video_author": "Test Author",
            "video_duration": "10:00",
            "publish_date": "2024-01-01",
            "view_count": "1000"
        }
    }
    
    try:
        print("📝 Testing /download-pdf endpoint...")
        response = requests.post(
            "http://localhost:8000/download-pdf",
            json=data,
            timeout=60
        )
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📄 Content-Type: {response.headers.get('content-type', 'Unknown')}")
        print(f"📏 Content-Length: {response.headers.get('content-length', 'Unknown')}")
        
        if response.status_code == 200:
            print("✅ PDF Download Successful!")
            print(f"📏 Size: {len(response.content)} bytes")
            
            # Save PDF
            filename = "download_test.pdf"
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

def test_both_endpoints():
    """Test both generate-pdf and download-pdf endpoints"""
    
    print("\n🔄 Testing both endpoints...")
    print("=" * 50)
    
    # Sample notes
    sample_notes = """# Test Notes

This is a test note for comparing endpoints."""

    data = {
        "notes": sample_notes,
        "title": "Endpoint Test",
        "youtube_url": "https://www.youtube.com/watch?v=test",
        "metadata": {}
    }
    
    endpoints = ["/generate-pdf", "/download-pdf"]
    
    for endpoint in endpoints:
        try:
            print(f"\n📝 Testing {endpoint}...")
            response = requests.post(
                f"http://localhost:8000{endpoint}",
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"✅ {endpoint} - Success! Size: {len(response.content)} bytes")
            else:
                print(f"❌ {endpoint} - Failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ {endpoint} - Exception: {e}")

if __name__ == "__main__":
    print("🚀 Download PDF Endpoint Test")
    print("=" * 60)
    
    test_download_pdf()
    test_both_endpoints() 