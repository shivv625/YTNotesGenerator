from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from utils import extract_transcript, generate_notes, generate_pdf  # ⬅️ import PDF function
import tempfile
import os

app = FastAPI(title="YouTube Notes Generator API", version="1.0.0")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, use your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body model
class VideoRequest(BaseModel):
    url: str

# PDF Request model
class PDFRequest(BaseModel):
    notes: str
    title: str
    youtube_url: str

# Response model
class NotesResponse(BaseModel):
    success: bool
    notes: str
    video_title: str | None = None
    video_author: str | None = None
    video_duration: str | None = None
    publish_date: str | None = None
    error: str | None = None

# ✅ Real route implementation
@app.post("/generate-notes/", response_model=NotesResponse)
async def create_notes(request: VideoRequest):
    try:
        # Validate URL
        if not request.url or not request.url.strip():
            raise HTTPException(status_code=400, detail="URL is required")
        
        # Step 1: Get transcript and metadata from YouTube video
        try:
            video_data = extract_transcript(request.url)
        except ValueError as e:
            # Invalid URL format
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            # Other transcript extraction errors
            error_msg = str(e)
            if "No transcript available" in error_msg:
                raise HTTPException(status_code=404, detail="No transcript available for this video. Please try a different video with subtitles enabled.")
            elif "Transcripts are disabled" in error_msg:
                raise HTTPException(status_code=403, detail="Transcripts are disabled for this video. The video owner has disabled subtitle generation.")
            elif "Video is unavailable" in error_msg:
                raise HTTPException(status_code=404, detail="Video is unavailable. It may be private, deleted, or restricted.")
            elif "Failed to fetch transcript" in error_msg:
                raise HTTPException(status_code=500, detail="Failed to fetch transcript. This might be due to language restrictions or video settings.")
            else:
                raise HTTPException(status_code=500, detail=f"Transcript extraction failed: {error_msg}")

        # Step 2: Generate notes using OpenRouter
        try:
            notes = await generate_notes(video_data["transcript"])
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Note generation failed: {str(e)}")

        # Step 3: Return result with metadata
        return NotesResponse(
            success=True,
            notes=notes,
            video_title=video_data.get("video_title"),
            video_author=video_data.get("video_author"),
            video_duration=video_data.get("video_duration"),
            publish_date=video_data.get("publish_date")
        )

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Catch any other unexpected errors
        return NotesResponse(
            success=False,
            notes="",
            error=f"Unexpected error: {str(e)}"
        )

# PDF Download endpoint
@app.post("/download-pdf/")
async def download_pdf(request: PDFRequest):
    try:
        # Generate PDF
        pdf_path = generate_pdf(request.notes, request.title, request.youtube_url)
        
        # Return the PDF file
        return FileResponse(
            path=pdf_path,
            filename=f"{request.title.replace(' ', '_')}.pdf",
            media_type="application/pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "YouTube Notes Generator API is running"}

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "YouTube Notes Generator API",
        "version": "1.0.0",
        "endpoints": {
            "generate_notes": "/generate-notes/",
            "download_pdf": "/download-pdf/",
            "health": "/health"
        }
    }
