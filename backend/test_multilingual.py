#!/usr/bin/env python3
"""
Test script for multilingual YouTube Notes Generator
"""

import asyncio
import httpx
import json

async def test_multilingual_notes():
    """Test the multilingual notes generation"""
    
    # Test URLs (you can replace these with actual YouTube URLs)
    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Example URL - replace with actual URLs
        # Add more test URLs here
    ]
    
    async with httpx.AsyncClient() as client:
        for url in test_urls:
            print(f"\n{'='*60}")
            print(f"Testing URL: {url}")
            print(f"{'='*60}")
            
            try:
                # Test the generate-notes endpoint
                response = await client.post(
                    "http://localhost:8000/generate-notes",
                    json={
                        "url": url,
                        "style": "comprehensive"
                    },
                    timeout=120.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Success!")
                    print(f"📺 Video Title: {data.get('video_title', 'Unknown')}")
                    print(f"👤 Author: {data.get('video_author', 'Unknown')}")
                    print(f"🌐 Transcript Language: {data.get('transcript_language', 'Unknown')}")
                    print(f"📝 Language Code: {data.get('transcript_language_code', 'Unknown')}")
                    print(f"⏱️ Duration: {data.get('video_duration', 'Unknown')}")
                    print(f"📊 View Count: {data.get('view_count', 'Unknown')}")
                    print(f"\n📋 Generated Notes Preview:")
                    print(f"{'='*40}")
                    
                    # Show first 500 characters of notes
                    notes = data.get('notes', '')
                    if notes:
                        print(notes[:500] + "..." if len(notes) > 500 else notes)
                    else:
                        print("No notes generated")
                        
                else:
                    print(f"❌ Error: {response.status_code}")
                    print(f"Response: {response.text}")
                    
            except Exception as e:
                print(f"❌ Exception: {str(e)}")
            
            print(f"\n{'='*60}\n")

async def test_health_check():
    """Test the health check endpoint"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://localhost:8000/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health Check: {data.get('status', 'Unknown')}")
                print(f"📝 Message: {data.get('message', 'Unknown')}")
                print(f"🔢 Version: {data.get('version', 'Unknown')}")
            else:
                print(f"❌ Health Check Failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Health Check Exception: {str(e)}")

async def test_available_styles():
    """Test the available styles endpoint"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://localhost:8000/styles")
            if response.status_code == 200:
                data = response.json()
                print(f"\n🎨 Available Note Styles:")
                for style in data.get('styles', []):
                    print(f"  • {style.get('name', 'Unknown')} ({style.get('value', 'Unknown')})")
            else:
                print(f"❌ Styles Check Failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Styles Check Exception: {str(e)}")

async def main():
    """Main test function"""
    print("🚀 YouTube Notes Generator - Multilingual Test")
    print("=" * 60)
    
    # Test health check first
    await test_health_check()
    
    # Test available styles
    await test_available_styles()
    
    # Test multilingual notes generation
    await test_multilingual_notes()
    
    print("\n✨ Test completed!")

if __name__ == "__main__":
    asyncio.run(main()) 