#!/usr/bin/env python3
"""
Debug script to test YouTube transcript extraction
"""

import sys
from utils import extract_transcript

def test_youtube_url(url):
    """Test transcript extraction for a given YouTube URL"""
    print(f"🧪 Testing YouTube URL: {url}")
    print("=" * 60)
    
    try:
        print("📡 Attempting to extract transcript...")
        result = extract_transcript(url)
        
        print("✅ Success!")
        print(f"📺 Video Title: {result.get('video_title', 'N/A')}")
        print(f"👤 Author: {result.get('video_author', 'N/A')}")
        print(f"⏱️ Duration: {result.get('video_duration', 'N/A')}")
        print(f"📅 Publish Date: {result.get('publish_date', 'N/A')}")
        print(f"🆔 Video ID: {result.get('video_id', 'N/A')}")
        print(f"📝 Transcript Length: {len(result.get('transcript', ''))} characters")
        
        # Show first 200 characters of transcript
        transcript = result.get('transcript', '')
        if transcript:
            print(f"📄 Transcript Preview: {transcript[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print(f"🔍 Error type: {type(e).__name__}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python debug_transcript.py <youtube_url>")
        print("Example: python debug_transcript.py https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        sys.exit(1)
    
    url = sys.argv[1]
    success = test_youtube_url(url)
    
    if success:
        print("\n✅ Transcript extraction successful!")
    else:
        print("\n❌ Transcript extraction failed!")
        print("\n💡 Common issues:")
        print("1. Video doesn't have subtitles/transcripts enabled")
        print("2. Video is private or restricted")
        print("3. Invalid YouTube URL format")
        print("4. Network connectivity issues")
        print("5. YouTube API rate limiting")

if __name__ == "__main__":
    main() 