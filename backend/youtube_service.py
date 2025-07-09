#!/usr/bin/env python3
"""
YouTube service for extracting transcripts and metadata
"""

import re
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from pytube import YouTube
from typing import Dict, Optional, List, Any, Union
import logging

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
    def get_transcript(video_id: str, languages: Optional[List[str]] = None) -> str:
        """Get transcript for a video ID with multilingual support"""
        try:
            # First, try to get available transcripts
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Try to get transcript in preferred languages or any available language
            transcript = None
            
            # Priority order for languages (English first, then others)
            preferred_languages = ['en', 'en-US', 'en-GB', 'en-CA', 'en-AU']
            
            # If specific languages are requested, try them first
            if languages:
                for lang in languages:
                    try:
                        transcript = transcript_list.find_transcript([lang])
                        break
                    except:
                        continue
            
            # If no specific language found, try preferred languages
            if not transcript:
                for lang in preferred_languages:
                    try:
                        transcript = transcript_list.find_transcript([lang])
                        break
                    except:
                        continue
            
            # If still no transcript, get the first available one
            if not transcript:
                transcript = list(transcript_list)[0]
            
            # Get the transcript text
            transcript_data = transcript.fetch()
            
            # Format transcript
            formatter = TextFormatter()
            transcript_text = formatter.format_transcript(transcript_data)
            
            return transcript_text
            
        except Exception as e:
            error_msg = str(e)
            if "No transcript available" in error_msg:
                raise Exception("No transcript available for this video. Please try a different video with subtitles enabled.")
            elif "Transcripts are disabled" in error_msg:
                raise Exception("Transcripts are disabled for this video. The video owner has disabled subtitle generation.")
            elif "Video is unavailable" in error_msg:
                raise Exception("Video is unavailable. It may be private, deleted, or restricted.")
            elif "Could not retrieve video" in error_msg:
                raise Exception("Could not retrieve video. It may be private or deleted.")
            else:
                raise Exception(f"Failed to fetch transcript: {error_msg}")
    
    @staticmethod
    def get_transcript_with_language_info(video_id: str) -> Dict[str, Union[str, bool]]:
        """Get transcript with language information"""
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Get the best available transcript
            transcript = None
            preferred_languages = ['en', 'en-US', 'en-GB', 'en-CA', 'en-AU']
            
            # Try preferred languages first
            for lang in preferred_languages:
                try:
                    transcript = transcript_list.find_transcript([lang])
                    break
                except:
                    continue
            
            # If no preferred language, get the first available one
            if not transcript:
                transcript = list(transcript_list)[0]
            
            # Get transcript data
            transcript_data = transcript.fetch()
            
            # Format transcript
            formatter = TextFormatter()
            transcript_text = formatter.format_transcript(transcript_data)
            
            return {
                "transcript": transcript_text,
                "language": transcript.language,
                "language_code": transcript.language_code,
                "is_generated": transcript.is_generated,
                "is_translatable": transcript.is_translatable
            }
            
        except Exception as e:
            raise Exception(f"Failed to fetch transcript with language info: {str(e)}")
    
    @staticmethod
    def get_video_metadata(url: str) -> Dict[str, Optional[str]]:
        """Get video metadata using pytube"""
        try:
            yt = YouTube(url)
            
            # Get basic metadata
            video_title = yt.title or "Unknown Title"
            video_author = yt.author or "Unknown Author"
            
            # Handle duration formatting
            if yt.length:
                minutes = yt.length // 60
                seconds = yt.length % 60
                video_duration = f"{minutes}:{seconds:02d}"
            else:
                video_duration = "Unknown"
            
            # Handle publish date
            if yt.publish_date:
                publish_date = yt.publish_date.strftime("%Y-%m-%d")
            else:
                publish_date = None
            
            # Get description (truncated)
            description = yt.description or ""
            if len(description) > 200:
                description = description[:200] + "..."
            
            # Get view count
            view_count = yt.views or 0
            
            return {
                "video_title": video_title,
                "video_author": video_author,
                "video_duration": video_duration,
                "publish_date": publish_date,
                "description": description,
                "view_count": str(view_count),
                "video_id": yt.video_id
            }
            
        except Exception as e:
            logger.warning(f"Could not fetch video metadata: {e}")
            return {
                "video_title": "Unknown Title",
                "video_author": "Unknown Author",
                "video_duration": "Unknown",
                "publish_date": None,
                "description": "",
                "view_count": "0",
                "video_id": None
            }
    
    @staticmethod
    def extract_transcript_and_metadata(url: str) -> Dict[str, Union[str, bool, None]]:
        """Extract both transcript and metadata from YouTube video with language support"""
        try:
            # Extract video ID
            video_id = YouTubeService.extract_video_id(url)
            
            # Get transcript with language information
            transcript_info = YouTubeService.get_transcript_with_language_info(video_id)
            
            # Get video metadata
            metadata = YouTubeService.get_video_metadata(url)
            
            return {
                "transcript": transcript_info["transcript"],
                "transcript_language": transcript_info["language"],
                "transcript_language_code": transcript_info["language_code"],
                "transcript_is_generated": transcript_info["is_generated"],
                "video_id": video_id,
                **metadata
            }
            
        except Exception as e:
            raise Exception(f"Failed to extract video data: {str(e)}")
    
    @staticmethod
    def validate_youtube_url(url: str) -> bool:
        """Validate if the URL is a valid YouTube URL"""
        try:
            video_id = YouTubeService.extract_video_id(url)
            return bool(video_id and len(video_id) == 11)
        except:
            return False 