from ast import pattern
import yt_dlp
import os
import uuid
import glob

# Groq Whisper processes audio to text. So the video is downloaded as mp3 first.
# yt_dlp logic for Instagram reels, posts, stories, etc.

def download_mp3(url: str) -> str:
    """
    Downloads audio from the given URL and returns the local MP3 file path.
    """

    # Create downloads folder if it doesn't exist
    os.makedirs("downloads", exist_ok=True)

    # Create cookies file from environment variable if it exists
    instagram_cookies = os.getenv("INSTAGRAM_COOKIES", "")
    if instagram_cookies:
        with open("instagram_cookies.txt", "w") as f:
            f.write(instagram_cookies)
        print("✅ Created instagram_cookies.txt from environment variable")

    # unique file name to avoid collisions
    file_id = str(uuid.uuid4())
    output_template = f"downloads/{file_id}.%(ext)s"

    ydl_opts = {
        # Best mp4 compatible format for n8n/social media
        'format': 'bestaudio/best',        
        'outtmpl': output_template,
        'quiet': False,  # Show output for debugging
        'no_warnings': False,  # Show warnings
        'cookiefile': 'instagram_cookies.txt',  # Use Instagram cookies for authentication
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    
        # FFMPEG

        #  'ffmpeg_location': '.',  # Adjust if ffmpeg is in a different location

        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128', # 128kbps é excelente para Whisper (fala) e mantém o arquivo pequeno
        }],
    }

    print(f"⬇️ Starting audio download for: {url}")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Download the audio and get info
        ydl.extract_info(url, download=True)
        
        pattern = f"downloads/{file_id}.mp3"
        matches = glob.glob(pattern)
        
        # Construct expected filename
        filename = f"downloads/{file_id}.mp3"

        if matches:
            filename = matches[0]
            print(f"✅ Audio downloaded successfully: {filename}")
            return filename
        else:
            # Fallback: Tenta achar qualquer extensão caso o post-processor falhe mas baixe algo
            fallback_pattern = f"downloads/{file_id}.*"
            matches = glob.glob(fallback_pattern)
            if matches:
                return matches[0]
            
            raise FileNotFoundError(f"Downloaded file not found. Expected pattern: {pattern}")

    return filename
    
# For Instagram, it is often necessary to use specific formatting options to ensure you get a single MP4 file that n8n can easily process.
# yt-dlp needs FFmpeg to merge high-quality video and audio. Even if you install yt-dlp with uv, you still need FFmpeg installed on your OS (via brew install ffmpeg, sudo apt install ffmpeg, etc.).