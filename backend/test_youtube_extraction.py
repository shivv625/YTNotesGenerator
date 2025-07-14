import sys
from youtube_transcript_api import YouTubeTranscriptApi
import pytube

video_url = sys.argv[1] if len(sys.argv) > 1 else input('Enter YouTube URL: ')
video_id = video_url.split('v=')[-1].split('&')[0] if 'v=' in video_url else video_url.split('/')[-1].split('?')[0]

print(f'Video ID: {video_id}')

# Test transcript extraction
try:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    print('✅ Transcript fetched successfully!')
    print('First 500 chars:', transcript[:500])
except Exception as e:
    print(f'❌ Transcript error: {e}')

# Test pytube metadata and audio
try:
    yt = pytube.YouTube(video_url)
    print('✅ pytube loaded video')
    print('Title:', yt.title)
    audio_stream = yt.streams.filter(only_audio=True).first()
    print('Audio stream found:', bool(audio_stream))
except Exception as e:
    print(f'❌ pytube error: {e}') 