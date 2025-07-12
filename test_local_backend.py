#!/usr/bin/env python3
"""
Test the backend locally to see the logs
"""

import requests
import json

def test_local_backend():
    """Test the backend running locally"""
    
    base_url = "http://localhost:8000"
    
    print("🔍 Testing Local Backend...")
    print("=" * 50)
    
    # Test with a video that has no captions
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    payload = {
        "url": test_url,
        "style": "comprehensive"
    }
    
    try:
        print(f"Testing with URL: {test_url}")
        response = requests.post(
            f"{base_url}/generate-notes",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Response status: {response.status_code}")
        data = response.json()
        
        if data.get("success"):
            print("✅ Note generation successful!")
            print(f"   Video title: {data.get('video_title', 'N/A')}")
            print(f"   Notes length: {len(data.get('notes', ''))} characters")
            print(f"   First 200 chars: {data.get('notes', '')[:200]}...")
        else:
            print(f"❌ Note generation failed: {data.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_local_backend() 