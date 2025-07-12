#!/usr/bin/env python3
"""
Test the YouTube service directly
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from youtube_service import YouTubeService

def test_youtube_service():
    """Test the YouTube service directly"""
    
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    print(f"Testing YouTube service with: {test_url}")
    print("=" * 50)
    
    try:
        result = YouTubeService.extract_transcript_and_metadata(test_url)
        print("✅ Success!")
        print(f"Video title: {result.get('video_title')}")
        print(f"Video author: {result.get('video_author')}")
        print(f"Transcript length: {len(result.get('transcript', ''))} characters")
        print(f"First 200 chars: {result.get('transcript', '')[:200]}...")
        print(f"Language: {result.get('transcript_language')}")
        
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    test_youtube_service() 