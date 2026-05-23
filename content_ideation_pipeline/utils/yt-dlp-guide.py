import yt_dlp
import os
import uuid

def download_video_locally(video_url):
    # Unique filename to avoid collisions
    file_id = str(uuid.uuid4())
    output_template = f"downloads/{file_id}.%(ext)s"
    
    ydl_opts = {
        # Best mp4 compatible format for n8n/social media
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': output_template,
        'quiet': True,
        'no_warnings': True,
    }

    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        # yt-dlp might change the extension (e.g., .mp4), so we get the final path
        filename = ydl.prepare_filename(info)
        return filename