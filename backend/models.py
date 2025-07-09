#!/usr/bin/env python3
"""
Pydantic models for request and response validation
"""

from pydantic import BaseModel, HttpUrl, validator
from typing import Optional, List
from enum import Enum

class NoteStyle(str, Enum):
    """Available note generation styles"""
    COMPREHENSIVE = "comprehensive"
    SUMMARY = "summary"
    DETAILED = "detailed"
    BULLET_POINTS = "bullet_points"

class VideoRequest(BaseModel):
    """Request model for video note generation"""
    url: str
    style: NoteStyle = NoteStyle.COMPREHENSIVE
    
    @validator('url')
    def validate_url(cls, v):
        if not v or not v.strip():
            raise ValueError("URL is required")
        return v.strip()

class PDFRequest(BaseModel):
    """Request model for PDF generation"""
    notes: str
    title: str
    youtube_url: str
    metadata: Optional[dict] = None
    
    @validator('notes')
    def validate_notes(cls, v):
        if not v or not v.strip():
            raise ValueError("Notes content is required")
        return v.strip()
    
    @validator('title')
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError("Title is required")
        return v.strip()

class NotesResponse(BaseModel):
    """Response model for note generation"""
    success: bool
    notes: str
    video_title: Optional[str] = None
    video_author: Optional[str] = None
    video_duration: Optional[str] = None
    publish_date: Optional[str] = None
    view_count: Optional[str] = None
    description: Optional[str] = None
    video_id: Optional[str] = None
    transcript_language: Optional[str] = None
    transcript_language_code: Optional[str] = None
    error: Optional[str] = None

class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str
    message: str
    version: str
    timestamp: str

class APIInfoResponse(BaseModel):
    """Response model for API information"""
    message: str
    version: str
    endpoints: dict
    features: List[str]

class ErrorResponse(BaseModel):
    """Response model for errors"""
    success: bool = False
    error: str
    details: Optional[str] = None 