#!/usr/bin/env python3
"""
Simple test example for the YouTube Notes Generator backend
"""

import asyncio
import httpx
import json

async def test_backend():
    """Test the backend API endpoints"""
    
    # Backend URL
    base_url = "http://localhost:8000"
    
    # Test video URL (replace with a real YouTube URL that has transcripts)
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll - has transcripts
    
    print("🧪 Testing YouTube Notes Generator Backend")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        
        # Test 1: Health Check
        print("\n1. Testing Health Check...")
        try:
            response = await client.get(f"{base_url}/health")
            if response.status_code == 200:
                print("✅ Health check passed")
                print(f"   Status: {response.json()['status']}")
                print(f"   Version: {response.json()['version']}")
            else:
                print(f"❌ Health check failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return
        
        # Test 2: Get Note Styles
        print("\n2. Testing Note Styles...")
        try:
            response = await client.get(f"{base_url}/styles")
            if response.status_code == 200:
                print("✅ Note styles retrieved")
                styles = response.json()['styles']
                for style in styles:
                    print(f"   - {style['name']}: {style['description']}")
            else:
                print(f"❌ Note styles failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Note styles error: {e}")
        
        # Test 3: Generate Notes
        print("\n3. Testing Note Generation...")
        try:
            payload = {
                "url": test_url,
                "style": "comprehensive"
            }
            response = await client.post(
                f"{base_url}/generate-notes/",
                json=payload,
                timeout=60.0
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    print("✅ Note generation successful")
                    print(f"   Video Title: {data.get('video_title', 'Unknown')}")
                    print(f"   Video Author: {data.get('video_author', 'Unknown')}")
                    print(f"   Duration: {data.get('video_duration', 'Unknown')}")
                    print(f"   Notes Length: {len(data['notes'])} characters")
                    
                    # Test 4: PDF Generation
                    print("\n4. Testing PDF Generation...")
                    pdf_payload = {
                        "notes": data['notes'],
                        "title": f"Notes: {data.get('video_title', 'Unknown Video')}",
                        "youtube_url": test_url,
                        "metadata": {
                            "video_title": data.get('video_title'),
                            "video_author": data.get('video_author'),
                            "video_duration": data.get('video_duration'),
                            "publish_date": data.get('publish_date'),
                            "view_count": data.get('view_count')
                        }
                    }
                    
                    pdf_response = await client.post(
                        f"{base_url}/download-pdf/",
                        json=pdf_payload,
                        timeout=30.0
                    )
                    
                    if pdf_response.status_code == 200:
                        print("✅ PDF generation successful")
                        print(f"   Content-Type: {pdf_response.headers.get('content-type')}")
                        print(f"   Content-Length: {pdf_response.headers.get('content-length')} bytes")
                    else:
                        print(f"❌ PDF generation failed: {pdf_response.status_code}")
                        print(f"   Error: {pdf_response.text}")
                else:
                    print(f"❌ Note generation failed: {data.get('error', 'Unknown error')}")
            else:
                print(f"❌ Note generation failed: {response.status_code}")
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"❌ Note generation error: {e}")
        
        # Test 5: API Info
        print("\n5. Testing API Info...")
        try:
            response = await client.get(f"{base_url}/")
            if response.status_code == 200:
                data = response.json()
                print("✅ API info retrieved")
                print(f"   Message: {data['message']}")
                print(f"   Version: {data['version']}")
                print(f"   Features: {len(data['features'])} features available")
            else:
                print(f"❌ API info failed: {response.status_code}")
        except Exception as e:
            print(f"❌ API info error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Testing completed!")

if __name__ == "__main__":
    print("Make sure the backend server is running on http://localhost:8000")
    print("You can start it with: python start_server.py")
    print()
    
    # Run the test
    asyncio.run(test_backend()) 