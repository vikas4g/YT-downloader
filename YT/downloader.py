import yt_dlp

# Global variable to store download progress
progress = {
    'percentage': 0,
    'status': 'idle'  # 'downloading', 'finished', 'error'
}

def get_video_info(url):
    with yt_dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)  # Don't download, just get info
        return info

# Function to print download progress
def progress_hook(d):
    global progress
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes', 0)
        downloaded_bytes = d.get('downloaded_bytes', 0)
        percentage = (downloaded_bytes / total_bytes) * 100 if total_bytes else 0
        progress['percentage'] = percentage
        progress['status'] = 'downloading'
    elif d['status'] == 'finished':
        progress['percentage'] = 100
        progress['status'] = 'finished'

# Function to download video or audio with progress hook
def download_video(url, format_type):
    global progress
    ydl_opts = {
        'format': 'bestaudio/best' if format_type == 'audio' else 'best',
        'outtmpl': 'download/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook]  # Add the progress hook here
    }

    progress['status'] = 'downloading'
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return f"{info['title']}.{info['ext']}"
