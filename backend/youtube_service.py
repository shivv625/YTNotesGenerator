#!/usr/bin/env python3
"""
YouTube service for extracting transcripts and metadata
"""

import re
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api._api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import pytube
from typing import Dict, Optional, List, Any, Union
import logging
import os
import tempfile
import traceback
import subprocess

logger = logging.getLogger(__name__)

class YouTubeService:
    """Service for YouTube video operations"""
    
    @staticmethod
    def extract_video_id(url: str) -> str:
        """Extract video ID from various YouTube URL formats"""
        try:
            parsed_url = urlparse(url)
            
            # Handle different YouTube URL formats
            if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
                if parsed_url.path == '/watch':
                    query_params = parse_qs(parsed_url.query)
                    if 'v' in query_params:
                        return query_params['v'][0]
                elif parsed_url.path.startswith('/embed/'):
                    return parsed_url.path.split('/')[2]
                elif parsed_url.path.startswith('/v/'):
                    return parsed_url.path.split('/')[2]
            elif parsed_url.hostname == 'youtu.be':
                return parsed_url.path[1:]
            elif parsed_url.hostname == 'm.youtube.com':
                if parsed_url.path == '/watch':
                    query_params = parse_qs(parsed_url.query)
                    if 'v' in query_params:
                        return query_params['v'][0]
            
            raise ValueError("Invalid YouTube URL format")
        except Exception as e:
            raise ValueError(f"Error parsing YouTube URL: {str(e)}")

    @staticmethod
    def extract_transcript_and_metadata(youtube_url: str):
        """
        Extract transcript and metadata from a YouTube video.
        Only uses YouTube transcript API, no Whisper fallback.
        """
        print(f"Starting transcript extraction for: {youtube_url}")
        
        # First, try to get video metadata (try pytube, fallback to minimal info)
        try:
            yt = pytube.YouTube(youtube_url)
            metadata = {
                "video_title": yt.title or "Unknown Title",
                "video_author": yt.author or "Unknown Author",
                "video_duration": str(yt.length) if yt.length else "Unknown",
                "publish_date": str(yt.publish_date) if yt.publish_date else None,
                "view_count": str(yt.views) if yt.views else "0",
                "description": yt.description or "",
                "video_id": yt.video_id
            }
        except Exception as e:
            print(f"Failed to get metadata: {e}")
            traceback.print_exc()
            # Fallback: try to extract video_id from URL
            try:
                video_id = YouTubeService.extract_video_id(youtube_url)
            except Exception:
                video_id = None
            metadata = {
                "video_title": "Unknown Title",
                "video_author": "Unknown Author", 
                "video_duration": "Unknown",
                "publish_date": None,
                "view_count": "0",
                "description": "",
                "video_id": video_id
            }
        # Try to get transcript first
        transcript = None
        transcript_language = "unknown"
        transcript_language_code = "unknown"
        try:
            print("Attempting to extract transcript...")
            video_id = metadata["video_id"] or YouTubeService.extract_video_id(youtube_url)
            transcript_info = YouTubeService.get_transcript_with_language_info(video_id)
            transcript = transcript_info["transcript"]
            transcript_language = transcript_info["language"]
            transcript_language_code = transcript_info["language_code"]
            print("✅ Transcript extracted successfully!")
        except Exception as e:
            print(f"❌ Transcript extraction failed: {e}")
            traceback.print_exc()
            raise Exception(f"Failed to extract video data. Transcript error: {e}")
        # Return the result
        return {
            "transcript": transcript,
            "transcript_language": transcript_language,
            "transcript_language_code": transcript_language_code,
            **metadata
        }

    @staticmethod
    def get_transcript_with_language_info(video_id: str) -> Dict[str, str]:
        """Get transcript and language info for a video ID"""
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = None
        language = "unknown"
        language_code = "unknown"
        # Prefer manually created transcript, then generated
        for t in transcript_list:
            if t.is_translatable:
                t = t.translate('en')
            if t.language_code == 'en' or t.language.lower() == 'english':
                transcript = t.fetch()
                language = t.language
                language_code = t.language_code
                break
        if transcript is None:
            # Fallback: just get the first transcript
            t = transcript_list.find_transcript([tr.language_code for tr in transcript_list])
            transcript = t.fetch()
            language = t.language
            language_code = t.language_code
        formatter = TextFormatter()
        transcript_text = formatter.format_transcript(transcript)
        return {
            "transcript": transcript_text,
            "language": language,
            "language_code": language_code
        }

    @staticmethod
    def validate_youtube_url(url: str) -> bool:
        """Validate if the URL is a valid YouTube URL"""
        try:
            video_id = YouTubeService.extract_video_id(url)
            return bool(video_id and len(video_id) == 11)
        except:
            return False 