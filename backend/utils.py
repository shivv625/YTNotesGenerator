import os
import httpx
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled, VideoUnavailable
from dotenv import load_dotenv
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
import tempfile

load_dotenv()
# Get API key from environment variable
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# If no API key in environment, use a fallback (you should set your own key)
if not OPENROUTER_API_KEY:
    OPENROUTER_API_KEY = "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"
    print("⚠️  Warning: Using fallback API key. For production, set OPENROUTER_API_KEY in .env file")

def extract_transcript(video_url: str) -> dict:
    try:
        # Validate URL format
        if not video_url or not isinstance(video_url, str):
            raise ValueError("Invalid URL: URL must be a non-empty string")
        
        # Create YouTube object
        try:
            yt = YouTube(video_url)
        except Exception as e:
            raise ValueError(f"Invalid YouTube URL: {str(e)}")
        
        # Extract video ID
        try:
            video_id = yt.video_id
            if not video_id:
                raise ValueError("Could not extract video ID from URL")
        except Exception as e:
            raise ValueError(f"Failed to extract video ID: {str(e)}")
        
        # Get transcript with better error handling and language support
        transcript = ""
        try:
            # First try to get transcript in any available language
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            if not transcript_list:
                raise NoTranscriptFound(video_id)
            
            # Join transcript chunks
            transcript = " ".join([chunk["text"] for chunk in transcript_list])
            
        except NoTranscriptFound:
            # Try to get transcript in specific languages with multiple fallbacks
            languages_to_try = [
                ['hi', 'hi-IN', 'hi-IN-IN'],  # Hindi variants
                ['en', 'en-US', 'en-GB', 'en-IN'],  # English variants
                ['auto'],  # Auto-generated
                ['hi', 'en'],  # Mixed Hindi/English
                ['en', 'hi']   # Mixed English/Hindi
            ]
            
            transcript_found = False
            for lang_list in languages_to_try:
                try:
                    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=lang_list)
                    transcript = " ".join([chunk["text"] for chunk in transcript_list])
                    transcript_found = True
                    break
                except:
                    continue
            
            if not transcript_found:
                raise Exception(f"No transcript available for video {video_id}. This video may not have subtitles enabled.")
                
        except TranscriptsDisabled:
            raise Exception(f"Transcripts are disabled for video {video_id}. The video owner has disabled subtitle generation.")
        except VideoUnavailable:
            raise Exception(f"Video {video_id} is unavailable. It may be private, deleted, or restricted.")
        except Exception as e:
            raise Exception(f"Failed to fetch transcript: {str(e)}")
        
        # Get video metadata with improved error handling
        try:
            # Force metadata fetch
            yt.check_availability()
            
            # Get title with fallback
            video_title = "Unknown Title"
            try:
                if yt.title:
                    video_title = yt.title.strip()
                elif hasattr(yt, 'initial_data') and yt.initial_data:
                    # Try to extract from initial data
                    import json
                    if 'videoDetails' in yt.initial_data:
                        video_title = yt.initial_data['videoDetails'].get('title', 'Unknown Title')
            except:
                pass
            
            # Get author/channel name with fallback
            video_author = "Unknown Author"
            try:
                if yt.author:
                    video_author = yt.author.strip()
                elif hasattr(yt, 'channel_name') and yt.channel_name:
                    video_author = yt.channel_name.strip()
                elif hasattr(yt, 'initial_data') and yt.initial_data:
                    # Try to extract from initial data
                    if 'videoDetails' in yt.initial_data:
                        video_author = yt.initial_data['videoDetails'].get('author', 'Unknown Author')
            except:
                pass
            
            # Get duration with proper formatting
            video_duration = "Unknown"
            try:
                if yt.length:
                    minutes = yt.length // 60
                    seconds = yt.length % 60
                    video_duration = f"{minutes}:{seconds:02d}"
            except:
                pass
            
            # Get publish date
            publish_date = None
            try:
                if yt.publish_date:
                    publish_date = yt.publish_date.strftime("%Y-%m-%d")
            except:
                pass
            
            metadata = {
                "transcript": transcript,
                "video_title": video_title,
                "video_author": video_author,
                "video_duration": video_duration,
                "publish_date": publish_date,
                "video_id": video_id
            }
            
        except Exception as e:
            # If metadata extraction fails, still return transcript with basic info
            print(f"Warning: Metadata extraction failed: {str(e)}")
            metadata = {
                "transcript": transcript,
                "video_title": "Unknown Title",
                "video_author": "Unknown Author", 
                "video_duration": "Unknown",
                "publish_date": None,
                "video_id": video_id
            }
        
        return metadata
    except Exception as e:
        # Re-raise with more context
        raise Exception(f"Failed to extract transcript: {str(e)}")

async def generate_notes(transcript: str) -> str:
    if not OPENROUTER_API_KEY or OPENROUTER_API_KEY == "your_new_api_key_here":
        # Fallback: Generate simple notes without API
        return generate_simple_notes(transcript)
    
    # Always generate notes in English, even if transcript is in Hindi
    prompt = f"""You are an expert note-taker and educator. Generate comprehensive, well-structured study notes in ENGLISH from this YouTube video transcript.\n\nIf the transcript is in Hindi or any other language, first understand it and then write the notes in clear, fluent English.\n\nPlease create notes that include:\n1. **Overview/Summary** - Brief introduction to the topic\n2. **Key Concepts** - Main ideas and important points\n3. **Detailed Explanations** - Important details with examples\n4. **Practical Applications** - How to apply the knowledge\n5. **Key Takeaways** - Summary of most important points\n\nUse clear markdown formatting with:\n- Headers (##, ###) for sections\n- Bullet points for lists\n- **Bold** for emphasis\n- Code blocks for technical terms\n- Clear organization and flow\n\nTranscript:\n{transcript}\n\nGenerate comprehensive, educational notes in English:"""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-site.com",
        "X-Title": "YouTube Notes Generator"
    }

    body = {
        "model": "nousresearch/deephermes-3-mistral-24b-preview:free",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 3000,
        "temperature": 0.7,
        "top_p": 0.9
    }

    try:
        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=body
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
    except httpx.TimeoutException:
        raise Exception("Request timed out. Please try again.")
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise Exception("Invalid API key. Please check your OpenRouter API key.")
        elif e.response.status_code == 429:
            raise Exception("Rate limit exceeded. Please try again later.")
        else:
            error_detail = e.response.text if e.response.text else f"Status: {e.response.status_code}"
            raise Exception(f"API request failed: {error_detail}")
    except Exception as e:
        raise Exception(f"Failed to generate notes: {str(e)}")

def generate_simple_notes(transcript: str) -> str:
    """Generate simple structured notes without AI API"""
    
    # Detect if transcript contains Hindi characters
    hindi_chars = set('अआइईउऊएऐओऔकखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहक्षत्रज्ञड़ढ़')
    sample_text = transcript[:200]
    is_hindi = any(char in hindi_chars for char in sample_text)
    
    if is_hindi:
        return f"""# 📝 वीडियो नोट्स

## 📋 सारांश
इस वीडियो में निम्नलिखित विषयों पर चर्चा की गई है:

## 🎯 मुख्य बिंदु
{generate_bullet_points(transcript, is_hindi=True)}

## 📚 विस्तृत नोट्स
{transcript[:1000]}...

## 💡 मुख्य सीख
- वीडियो से प्राप्त ज्ञान को व्यवहार में लाएं
- महत्वपूर्ण बिंदुओं को याद रखें
- आगे के अध्ययन के लिए नोट्स का उपयोग करें

---
*ये नोट्स YouTube वीडियो से स्वचालित रूप से तैयार किए गए हैं।*"""
    else:
        return f"""# 📝 Video Notes

## 📋 Summary
This video covers the following topics:

## 🎯 Key Points
{generate_bullet_points(transcript, is_hindi=False)}

## 📚 Detailed Notes
{transcript[:1000]}...

## 💡 Key Takeaways
- Apply the knowledge gained from the video
- Remember the important points
- Use these notes for further study

---
*These notes were automatically generated from the YouTube video.*"""

def generate_bullet_points(transcript: str, is_hindi: bool = False) -> str:
    """Generate bullet points from transcript"""
    sentences = transcript.split('.')
    key_points = []
    
    for sentence in sentences[:10]:  # Take first 10 sentences
        sentence = sentence.strip()
        if len(sentence) > 20:  # Only meaningful sentences
            key_points.append(f"- {sentence}")
    
    return '\n'.join(key_points[:5])  # Return top 5 points

def generate_pdf(notes: str, title: str, youtube_url: str) -> str:
    """Generate a PDF file from the notes"""
    try:
        # Create a temporary file for the PDF
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        pdf_path = temp_file.name
        temp_file.close()
        
        # Create the PDF document
        doc = SimpleDocTemplate(pdf_path, pagesize=A4)
        story = []
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Create custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=HexColor('#1f2937'),
            alignment=1  # Center alignment
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=20,
            textColor=HexColor('#6b7280'),
            alignment=1  # Center alignment
        )
        
        header_style = ParagraphStyle(
            'CustomHeader',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=HexColor('#1f2937')
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            textColor=HexColor('#374151'),
            leading=16
        )
        
        # Add title
        story.append(Paragraph(f"<b>{title}</b>", title_style))
        story.append(Spacer(1, 12))
        
        # Add subtitle with YouTube URL
        story.append(Paragraph(f"Generated from: {youtube_url}", subtitle_style))
        story.append(Spacer(1, 20))
        
        # Add generation date
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", subtitle_style))
        story.append(PageBreak())
        
        # Process notes content
        lines = notes.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                story.append(Spacer(1, 6))
                continue
                
            # Check if it's a header
            if line.startswith('##'):
                # Main header
                header_text = line.replace('#', '').strip()
                story.append(Paragraph(f"<b>{header_text}</b>", header_style))
            elif line.startswith('###'):
                # Sub header
                header_text = line.replace('#', '').strip()
                story.append(Paragraph(f"<b>{header_text}</b>", header_style))
            elif line.startswith('**') and line.endswith('**'):
                # Bold text
                bold_text = line.replace('**', '')
                story.append(Paragraph(f"<b>{bold_text}</b>", body_style))
            elif line.startswith('- ') or line.startswith('* '):
                # Bullet point
                bullet_text = line[2:].strip()
                story.append(Paragraph(f"• {bullet_text}", body_style))
            else:
                # Regular text
                story.append(Paragraph(line, body_style))
        
        # Build the PDF
        doc.build(story)
        
        return pdf_path
        
    except Exception as e:
        raise Exception(f"Failed to generate PDF: {str(e)}")
