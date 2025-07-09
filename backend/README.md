# YouTube Notes Generator Backend

A powerful FastAPI backend that generates comprehensive study notes from YouTube videos using AI.

## Features

- **YouTube Transcript Extraction**: Automatically extracts transcripts from YouTube videos
- **AI-Powered Note Generation**: Uses OpenRouter API with Mistral AI for intelligent note generation
- **Multiple Note Styles**:
  - Comprehensive (detailed with overview, concepts, explanations, applications, takeaways)
  - Summary (concise overview with key points)
  - Detailed (extensive notes with technical details and examples)
  - Bullet Points (easy-to-scan format)
- **PDF Generation**: Creates beautifully formatted PDF documents with metadata
- **Video Metadata**: Extracts title, author, duration, publish date, view count, and description
- **Error Handling**: Comprehensive error handling with fallback mechanisms
- **CORS Support**: Full CORS support for frontend integration
- **Async Processing**: Non-blocking async operations for better performance

## Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd YTNotesGeneratorFrontend/backend
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the backend directory:
   ```env
   OPENROUTER_API_KEY=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
   ```

## Usage

### Starting the Server

```bash
# Using the startup script
python start_server.py

# Or directly with uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### API Endpoints

#### 1. Generate Notes

```http
POST /generate-notes/
Content-Type: application/json

{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "style": "comprehensive"
}
```

**Response**:

```json
{
  "success": true,
  "notes": "## Overview/Summary\n...",
  "video_title": "Video Title",
  "video_author": "Channel Name",
  "video_duration": "10:30",
  "publish_date": "2024-01-15",
  "view_count": "1000000",
  "description": "Video description...",
  "video_id": "VIDEO_ID"
}
```

#### 2. Download PDF

```http
POST /download-pdf/
Content-Type: application/json

{
  "notes": "Generated notes content...",
  "title": "My Study Notes",
  "youtube_url": "https://www.youtube.com/watch?v=VIDEO_ID",
  "metadata": {
    "video_title": "Video Title",
    "video_author": "Channel Name",
    "video_duration": "10:30",
    "publish_date": "2024-01-15",
    "view_count": "1000000"
  }
}
```

#### 3. Health Check

```http
GET /health
```

#### 4. Get Note Styles

```http
GET /styles
```

#### 5. API Information

```http
GET /
```

## API Documentation

Once the server is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Project Structure

```
backend/
├── main.py              # FastAPI application
├── config.py            # Configuration settings
├── models.py            # Pydantic models
├── youtube_service.py   # YouTube transcript extraction
├── ai_service.py        # AI note generation
├── pdf_service.py       # PDF generation
├── start_server.py      # Server startup script
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Configuration

The application uses a `Config` class in `config.py` for all settings:

- **API Keys**: OpenRouter API key for AI services
- **Request Limits**: Maximum transcript length, tokens, etc.
- **PDF Settings**: Page size, margins, formatting
- **CORS Settings**: Allowed origins
- **Timeout Settings**: Request and API timeouts

## Error Handling

The application includes comprehensive error handling:

- **Invalid URLs**: Returns 400 with clear error message
- **No Transcripts**: Returns 404 with helpful guidance
- **API Failures**: Falls back to simple note generation
- **Rate Limiting**: Handles OpenRouter rate limits gracefully
- **Network Issues**: Timeout handling and retry logic

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest
```

### Code Style

The project follows PEP 8 standards. Use a linter like `flake8` or `black` for code formatting.

## Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables

- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: 0.0.0.0)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
