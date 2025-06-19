#!/usr/bin/env python3
"""
Test script to verify backend server is running
"""

import requests
import json
import sys

def test_backend_health():
    """Test if the backend server is running"""
    try:
        print("🏥 Testing backend health...")
        response = requests.get("http://localhost:8000/health", timeout=5)
        
        if response.status_code == 200:
            print("✅ Backend server is running!")
            print(f"📄 Response: {response.json()}")
            return True
        else:
            print(f"❌ Backend responded with status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend server at http://localhost:8000")
        print("💡 Make sure the backend server is running with: python main.py")
        return False
    except Exception as e:
        print(f"❌ Error testing backend: {str(e)}")
        return False

def test_generate_notes_endpoint():
    """Test the generate-notes endpoint with a sample URL"""
    try:
        print("\n🧪 Testing generate-notes endpoint...")
        
        # Test with a sample YouTube URL (you can change this)
        test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll for testing
        
        payload = {"url": test_url}
        headers = {"Content-Type": "application/json"}
        
        print(f"📡 Sending request to /generate-notes/ with URL: {test_url}")
        
        response = requests.post(
            "http://localhost:8000/generate-notes/",
            json=payload,
            headers=headers,
            timeout=30
        )
        
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✅ Note generation successful!")
                print(f"📺 Video Title: {data.get('video_title', 'N/A')}")
                print(f"👤 Author: {data.get('video_author', 'N/A')}")
                print(f"📝 Notes length: {len(data.get('notes', ''))} characters")
                return True
            else:
                print(f"❌ Note generation failed: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP Error {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out (30 seconds)")
        return False
    except Exception as e:
        print(f"❌ Error testing endpoint: {str(e)}")
        return False

def main():
    print("🚀 YouTube Notes Generator - Backend Test")
    print("=" * 50)
    
    # Test if backend is running
    if not test_backend_health():
        print("\n❌ Backend server is not running!")
        print("💡 Start the backend with: python main.py")
        sys.exit(1)
    
    # Test the generate-notes endpoint
    success = test_generate_notes_endpoint()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ All backend tests passed!")
        print("🎉 Your backend is working correctly.")
    else:
        print("❌ Backend tests failed.")
        print("🔧 Check the error messages above for troubleshooting.")

if __name__ == "__main__":
    main() 