#!/usr/bin/env python3
"""
Full workflow test: YouTube URL → Notes → PDF Download
"""

import requests
import json
import time

def test_full_workflow():
    """Test the complete workflow from YouTube URL to PDF"""
    
    # Test with a real YouTube URL (replace with actual URL)
    youtube_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Example URL
    
    print("🚀 YouTube Notes Generator - Full Workflow Test")
    print("=" * 60)
    
    try:
        # Step 1: Generate notes from YouTube URL
        print("📝 Step 1: Generating notes from YouTube URL...")
        print(f"🔗 URL: {youtube_url}")
        
        notes_response = requests.post(
            "http://localhost:8000/generate-notes",
            json={
                "url": youtube_url,
                "style": "comprehensive"
            },
            timeout=120
        )
        
        if notes_response.status_code == 200:
            notes_data = notes_response.json()
            print("✅ Notes generated successfully!")
            print(f"📺 Video Title: {notes_data.get('video_title', 'Unknown')}")
            print(f"👤 Author: {notes_data.get('video_author', 'Unknown')}")
            print(f"🌐 Language: {notes_data.get('transcript_language', 'Unknown')}")
            print(f"⏱️ Duration: {notes_data.get('video_duration', 'Unknown')}")
            
            # Step 2: Generate PDF from the notes
            print("\n📄 Step 2: Generating PDF from notes...")
            
            pdf_response = requests.post(
                "http://localhost:8000/generate-pdf",
                json={
                    "notes": notes_data["notes"],
                    "title": notes_data.get("video_title", "YouTube Notes"),
                    "youtube_url": youtube_url,
                    "metadata": {
                        "video_author": notes_data.get("video_author"),
                        "video_duration": notes_data.get("video_duration"),
                        "publish_date": notes_data.get("publish_date"),
                        "view_count": notes_data.get("view_count")
                    }
                },
                timeout=60
            )
            
            if pdf_response.status_code == 200:
                print("✅ PDF generated successfully!")
                print(f"📄 Content-Type: {pdf_response.headers.get('content-type')}")
                print(f"📏 File Size: {len(pdf_response.content)} bytes")
                
                # Save the PDF with a descriptive filename
                filename = f"youtube_notes_{notes_data.get('video_id', 'unknown')}.pdf"
                with open(filename, "wb") as f:
                    f.write(pdf_response.content)
                
                print(f"💾 PDF saved as: {filename}")
                print(f"📁 File size: {len(pdf_response.content)} bytes")
                
                # Step 3: Show notes preview
                print(f"\n📋 Notes Preview (first 300 characters):")
                print("-" * 40)
                notes_preview = notes_data.get("notes", "")[:300]
                print(notes_preview + "..." if len(notes_data.get("notes", "")) > 300 else notes_preview)
                
                print(f"\n✨ Full workflow completed successfully!")
                print(f"📖 You can now open {filename} to view your notes!")
                
            else:
                print(f"❌ PDF Generation Failed: {pdf_response.status_code}")
                print(f"Response: {pdf_response.text}")
                
        else:
            print(f"❌ Notes Generation Failed: {notes_response.status_code}")
            print(f"Response: {notes_response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out. The video might be too long or the server is slow.")
    except requests.exceptions.ConnectionError:
        print("❌ Connection error. Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

def test_health_check():
    """Test if the server is running"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Server is running: {data.get('status')}")
            return True
        else:
            print(f"❌ Server health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to server: {str(e)}")
        return False

def main():
    """Main function"""
    print("🔍 Checking server status...")
    
    if not test_health_check():
        print("\n❌ Server is not running. Please start the server first:")
        print("   cd backend")
        print("   uvicorn main:app --reload")
        return
    
    print("\n" + "="*60)
    test_full_workflow()

if __name__ == "__main__":
    main() 