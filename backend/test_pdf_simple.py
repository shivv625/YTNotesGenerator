#!/usr/bin/env python3
"""
Simple test for PDF generation
"""

import requests
import json

def test_pdf():
    """Test PDF generation"""
    
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
        print("🧪 Testing PDF Generation...")
        response = requests.post(
            "http://localhost:8000/generate-pdf",
            json=data,
            timeout=60
        )
        
        if response.status_code == 200:
            print("✅ PDF Generated Successfully!")
            print(f"📄 Content-Type: {response.headers.get('content-type')}")
            print(f"📏 Size: {len(response.content)} bytes")
            
            # Save PDF
            with open("test_notes.pdf", "wb") as f:
                f.write(response.content)
            print("💾 PDF saved as test_notes.pdf")
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_pdf() 