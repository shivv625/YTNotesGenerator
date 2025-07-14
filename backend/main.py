#!/usr/bin/env 
"""
YouTube Notes Generator Backend - FastAPI Application
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import asyncio
import os
from datetime import datetime
from typing import Optional

# Import our services and models
from models import (
    VideoRequest, PDFRequest, NotesResponse, HealthResponse, 
    APIInfoResponse, ErrorResponse, NoteStyle
)
from youtube_service import YouTubeService
from ai_service import AIService
from pdf_service import PDFService
from config import Config

# Create FastAPI app
app = FastAPI(
    title="YouTube Notes Generator API",
    description="Generate comprehensive study notes from YouTube videos using AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware with configured origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_model=APIInfoResponse)
async def root():
    """Root endpoint with API information"""
    return APIInfoResponse(
        message="YouTube Notes Generator API",
        version="1.0.0",
        endpoints={
            "generate_notes": "/generate-notes",
            "generate_pdf": "/generate-pdf",
            "download_pdf": "/download-pdf",
            "health": "/health",
            "docs": "/docs"
        },
        features=[
            "YouTube video transcript extraction",
            "AI-powered note generation",
            "Multiple note styles (comprehensive, summary, detailed, bullet points)",
            "PDF generation with formatting",
            "Video metadata extraction"
        ]
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="YouTube Notes Generator API is running",
        version="1.0.0",
        timestamp=datetime.now().isoformat()
    )

@app.post("/generate-notes", response_model=NotesResponse)
async def generate_notes(request: VideoRequest):
    """Generate notes from a YouTube video"""
    try:
        # Validate YouTube URL
        if not YouTubeService.validate_youtube_url(request.url):
            raise HTTPException(status_code=400, detail="Invalid YouTube URL")
        
        # Extract transcript and metadata
        video_data = YouTubeService.extract_transcript_and_metadata(request.url)
        
        # Get transcript language for AI processing
        transcript_language = str(video_data.get("transcript_language", "unknown"))
        
        # Generate notes using AI with language information
        notes = await AIService.generate_notes(
            str(video_data["transcript"]), 
            request.style.value,
            transcript_language
        )
        
        return NotesResponse(
            success=True,
            notes=notes,
            video_title=str(video_data.get("video_title")) if video_data.get("video_title") else None,
            video_author=str(video_data.get("video_author")) if video_data.get("video_author") else None,
            video_duration=str(video_data.get("video_duration")) if video_data.get("video_duration") else None,
            publish_date=str(video_data.get("publish_date")) if video_data.get("publish_date") else None,
            view_count=str(video_data.get("view_count")) if video_data.get("view_count") else None,
            description=str(video_data.get("description")) if video_data.get("description") else None,
            video_id=str(video_data.get("video_id")) if video_data.get("video_id") else None,
            transcript_language=str(video_data.get("transcript_language")) if video_data.get("transcript_language") else None,
            transcript_language_code=str(video_data.get("transcript_language_code")) if video_data.get("transcript_language_code") else None
        )
        
    except Exception as e:
        return NotesResponse(
            success=False,
            notes="",
            error=str(e)
        )

@app.post("/generate-pdf")
async def generate_pdf(request: PDFRequest):
    """Generate PDF from notes"""
    try:
        # Generate PDF
        pdf_path = PDFService.generate_pdf(
            notes=request.notes,
            title=request.title,
            youtube_url=request.youtube_url,
            metadata=request.metadata or {}
        )
        
        # Return PDF file
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"{request.title.replace(' ', '_')}.pdf"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

@app.post("/download-pdf")
async def download_pdf(request: PDFRequest):
    """Download PDF from notes (alias for generate-pdf)"""
    try:
        # Generate PDF
        pdf_path = PDFService.generate_pdf(
            notes=request.notes,
            title=request.title,
            youtube_url=request.youtube_url,
            metadata=request.metadata or {}
        )
        
        # Return PDF file
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"{request.title.replace(' ', '_')}.pdf"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

@app.get("/styles")
async def get_available_styles():
    """Get available note generation styles"""
    return {
        "styles": [
            {"value": style.value, "name": style.name.replace("_", " ").title()}
            for style in NoteStyle
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 