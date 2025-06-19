#!/usr/bin/env python3
"""
Test script to verify Hindi video processing
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import extract_transcript, generate_notes

async def test_hindi_video():
    """Test Hindi video processing"""
    
    # Test with a Hindi video URL (replace with actual Hindi video URL)
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Replace with Hindi video
    
    print("🧪 Testing Hindi video processing...")
    print(f"URL: {test_url}")
    
    try:
        # Test transcript extraction
        print("\n📝 Extracting transcript...")
        video_data = extract_transcript(test_url)
        
        print(f"✅ Transcript extracted successfully!")
        print(f"📺 Video Title: {video_data.get('video_title', 'Unknown')}")
        print(f"👤 Channel: {video_data.get('video_author', 'Unknown')}")
        print(f"⏱️ Duration: {video_data.get('video_duration', 'Unknown')}")
        print(f"📅 Published: {video_data.get('publish_date', 'Unknown')}")
        print(f"📄 Transcript length: {len(video_data.get('transcript', ''))} characters")
        
        # Test note generation
        print("\n🤖 Generating notes...")
        notes = await generate_notes(video_data["transcript"])
        
        print(f"✅ Notes generated successfully!")
        print(f"📝 Notes length: {len(notes)} characters")
        print(f"📄 First 200 chars: {notes[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    asyncio.run(test_hindi_video()) 