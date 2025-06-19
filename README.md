# YouTube Notes Generator

An AI-powered web application that generates comprehensive study notes from YouTube videos. Built with React (Frontend) and FastAPI (Backend).

## Features

- 🎥 Extract transcripts from any YouTube video
- 🤖 Generate AI-powered study notes using OpenRouter
- 📝 Structured notes with markdown formatting
- 📱 Modern, responsive UI
- 📄 Export notes (PDF functionality coming soon)
- ⚡ Fast and efficient processing

## Prerequisites

- Python 3.8+
- Node.js 16+
- OpenRouter API key (free tier available)

## Setup Instructions

### 1. Backend Setup

1. Navigate to the backend directory:

   ```bash
   cd backend
   ```

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:

   ```bash
   # Copy the example file
   cp env_example.txt .env

   # Edit .env and add your OpenRouter API key
   # Get your API key from: https://openrouter.ai/
   ```

4. Run the backend server:

   ```bash
   python run.py
   ```

   The backend will be available at: http://localhost:8000

### 2. Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:

   ```bash
   npm install
   ```

3. Start the development server:

   ```bash
   npm run dev
   ```

   The frontend will be available at: http://localhost:5173

## API Endpoints

- `POST /generate-notes/` - Generate notes from YouTube URL
- `GET /health` - Health check endpoint
- `GET /` - API information

## Usage

1. Open the application in your browser (http://localhost:5173)
2. Paste a YouTube video URL
3. Click "Generate Notes"
4. Wait for the AI to process the video and generate notes
5. View and download your notes

## Project Structure

```
YTNotesGeneratorFrontend/
├── backend/
│   ├── main.py          # FastAPI application
│   ├── utils.py         # Utility functions
│   ├── requirements.txt # Python dependencies
│   ├── run.py          # Server startup script
│   └── env_example.txt # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── App.tsx     # Main React component
│   │   └── main.tsx    # React entry point
│   ├── package.json    # Node.js dependencies
│   └── vite.config.ts  # Vite configuration
└── README.md           # This file
```

## Technologies Used

### Backend

- **FastAPI** - Modern Python web framework
- **Pytube** - YouTube video processing
- **YouTube Transcript API** - Extract video transcripts
- **OpenRouter** - AI model API for note generation
- **httpx** - Async HTTP client

### Frontend

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Styling
- **Lucide React** - Icons

## Troubleshooting

### Common Issues

1. **"Failed to extract transcript"**

   - Make sure the YouTube video has captions/transcripts available
   - Check if the video URL is valid

2. **"Invalid API key"**

   - Verify your OpenRouter API key is correct
   - Make sure the `.env` file is in the backend directory

3. **"Failed to connect to server"**

   - Ensure the backend is running on port 8000
   - Check if there are any firewall issues

4. **CORS errors**
   - The backend is configured to allow all origins in development
   - For production, update the CORS settings in `main.py`

### Getting an OpenRouter API Key

1. Visit [OpenRouter](https://openrouter.ai/)
2. Sign up for a free account
3. Navigate to your API keys section
4. Create a new API key
5. Copy the key to your `.env` file

## Development

### Running in Development Mode

Both frontend and backend support hot reloading:

- Backend: `python run.py` (auto-reloads on file changes)
- Frontend: `npm run dev` (Vite dev server with HMR)

### Building for Production

1. Build the frontend:

   ```bash
   cd frontend
   npm run build
   ```

2. The built files will be in `frontend/dist/`

## License

This project is open source and available under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

If you encounter any issues or have questions, please open an issue on the repository.
