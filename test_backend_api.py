#!/usr/bin/env python3
"""
Test script for the backend API
"""

import requests
import json

def test_backend_api():
    """Test the backend API endpoints"""
    
    base_url = "https://brevixai-backend.onrender.com"
    
    print("🔍 Testing Backend API...")
    print("=" * 50)
    
    # Test 1: Health check
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            print(f"   Message: {data['message']}")
            print(f"   Version: {data['version']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    print("\n" + "=" * 50)
    
    # Test 2: API info
    print("2. Testing API info endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API info: {data['message']}")
            print(f"   Version: {data['version']}")
            print(f"   Available endpoints: {list(data['endpoints'].keys())}")
        else:
            print(f"❌ API info failed: {response.status_code}")
    except Exception as e:
        print(f"❌ API info error: {e}")
    
    print("\n" + "=" * 50)
    
    # Test 3: Note generation
    print("3. Testing note generation...")
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll - no captions
    
    payload = {
        "url": test_url,
        "style": "comprehensive"
    }
    
    try:
        print(f"   Testing with URL: {test_url}")
        response = requests.post(
            f"{base_url}/generate-notes",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                print("✅ Note generation successful!")
                print(f"   Video title: {data.get('video_title', 'N/A')}")
                print(f"   Video author: {data.get('video_author', 'N/A')}")
                print(f"   Notes length: {len(data.get('notes', ''))} characters")
                print(f"   First 200 chars of notes: {data.get('notes', '')[:200]}...")
            else:
                print(f"❌ Note generation failed: {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ Note generation failed with status: {response.status_code}")
            try:
                error_data = response.json()
                print(f"   Error details: {error_data}")
            except:
                print(f"   Response text: {response.text}")
    except Exception as e:
        print(f"❌ Note generation error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Testing complete!")

if __name__ == "__main__":
    test_backend_api() 