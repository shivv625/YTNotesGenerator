# YouTube Notes Generator - Troubleshooting Guide

## Common Issues and Solutions

### 1. "Failed to extract transcript: HTTP Error 400: Bad Request"

This error typically occurs when there are issues with the YouTube URL or transcript extraction. Here are the most common causes and solutions:

#### **A. Backend Server Not Running**

**Symptoms:** HTTP 400 error or connection refused
**Solution:**

1. Make sure the backend server is running:
   ```bash
   cd backend
   python main.py
   ```
2. Or use the batch file:
   ```bash
   start_servers.bat
   ```

#### **B. Invalid YouTube URL**

**Symptoms:** HTTP 400 error with "Invalid YouTube URL" message
**Solutions:**

1. Make sure the URL is a valid YouTube video URL
2. Supported formats:
   - `https://www.youtube.com/watch?v=VIDEO_ID`
   - `https://youtu.be/VIDEO_ID`
   - `https://youtube.com/watch?v=VIDEO_ID`
3. Avoid URLs with extra parameters or timestamps

#### **C. Video Has No Transcripts**

**Symptoms:** HTTP 404 error with "No transcript available" message
**Solutions:**

1. Try a different YouTube video that has subtitles/transcripts enabled
2. Look for videos with the "CC" (Closed Captions) button
3. Educational videos typically have better transcript availability

#### **D. Video is Private/Restricted**

**Symptoms:** HTTP 404 error with "Video is unavailable" message
**Solutions:**

1. Make sure the video is public
2. Try a different video URL
3. Check if the video requires authentication

#### **E. Transcripts Disabled by Creator**

**Symptoms:** HTTP 403 error with "Transcripts are disabled" message
**Solutions:**

1. Try a different video
2. Look for videos with auto-generated or manual subtitles

### 2. PDF Download Issues

#### **A. PDF Not Generating**

**Symptoms:** PDF download button doesn't work or shows error
**Solutions:**

1. Make sure the backend server is running
2. Check that the `reportlab` library is installed:
   ```bash
   cd backend
   pip install reportlab
   ```
3. Test PDF generation:
   ```bash
   cd backend
   python test_pdf.py
   ```

#### **B. PDF Download Fails**

**Symptoms:** Error message when trying to download PDF
**Solutions:**

1. Check browser console for error messages
2. Ensure you have generated notes before trying to download
3. Try refreshing the page and generating notes again
4. Check if your browser allows downloads

#### **C. PDF File is Empty or Corrupted**

**Symptoms:** PDF downloads but is empty or won't open
**Solutions:**

1. Make sure the notes were generated successfully
2. Try generating notes from a different video
3. Check if the video title contains special characters

### 3. Hindi Language Support

#### **A. Hindi Videos Not Working**

**Symptoms:** Hindi videos show errors or don't generate notes
**Solutions:**

1. Make sure the Hindi video has subtitles/transcripts enabled
2. The system automatically detects Hindi content
3. Notes will be generated in Hindi with proper formatting
4. Try videos from popular Hindi educational channels

#### **B. Mixed Language Content**

**Symptoms:** Videos with mixed Hindi-English content
**Solutions:**

1. The system will detect the primary language
2. Notes will be generated in the detected language
3. For best results, use videos primarily in one language

### 4. Testing and Debugging

#### **Test Backend Health**

```bash
cd backend
python test_backend.py
```

#### **Test Specific YouTube URL**

```bash
cd backend
python debug_transcript.py "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"
```

#### **Test API Connection**

```bash
cd backend
python test_api.py
```

#### **Test PDF Generation**

```bash
cd backend
python test_pdf.py
```

### 5. Installation Issues

#### **Missing Dependencies**

If you get import errors, install the requirements:

```bash
cd backend
pip install -r requirements.txt
```

#### **Python Version**

Make sure you're using Python 3.7 or higher:

```bash
python --version
```

### 6. Network Issues

#### **Firewall/Antivirus**

- Temporarily disable firewall/antivirus to test
- Add exceptions for the application

#### **Proxy Settings**

- If behind a corporate proxy, configure proxy settings
- Check if YouTube is accessible from your network

### 7. Rate Limiting

#### **YouTube API Limits**

- YouTube may rate limit requests if too many are made
- Wait a few minutes and try again
- Use different videos for testing

#### **OpenRouter API Limits**

- Check your OpenRouter API key usage
- The free tier has rate limits

### 8. Frontend Issues

#### **CORS Errors**

- Make sure the backend is running on port 8000
- Check that the Vite proxy is configured correctly
- Frontend should be on port 5173

#### **Connection Refused**

- Verify both servers are running
- Check console for error messages
- Restart both frontend and backend

### 9. Step-by-Step Debugging

1. **Start Fresh:**

   ```bash
   # Stop all running servers
   # Close all terminal windows
   ```

2. **Start Backend:**

   ```bash
   cd backend
   python main.py
   ```

3. **Test Backend:**

   ```bash
   # In a new terminal
   cd backend
   python test_backend.py
   ```

4. **Test PDF Generation:**

   ```bash
   # In a new terminal
   cd backend
   python test_pdf.py
   ```

5. **Start Frontend:**

   ```bash
   cd frontend
   npm run dev
   ```

6. **Test with Known Good URL:**
   - Use a popular educational video
   - Make sure it has subtitles enabled
   - Example: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`

### 10. Getting Help

If you're still having issues:

1. **Check the console logs** in both frontend and backend terminals
2. **Run the test scripts** to identify the specific issue
3. **Try with a different YouTube video** to isolate the problem
4. **Check your internet connection** and firewall settings

### 11. Common YouTube URLs That Work

For testing, try these videos that typically have good transcripts:

- Educational content from channels like Khan Academy, MIT OpenCourseWare
- TED Talks
- Programming tutorials
- Academic lectures
- Hindi educational channels (for Hindi support testing)

### 12. Environment Variables

Make sure your `.env` file is set up correctly:

```env
OPENROUTER_API_KEY=your_api_key_here
```

The API key in the code is for testing only. For production, use your own OpenRouter API key.

### 13. Language Support

The application now supports:

- **English** - Primary language with full support
- **Hindi** - Automatic detection and Hindi note generation
- **Other languages** - Basic support for other languages with transcripts

For best results with Hindi videos:

1. Use videos with Hindi subtitles/transcripts
2. The system will automatically detect Hindi content
3. Notes will be generated in Hindi with proper formatting
4. PDF downloads work with Hindi content
