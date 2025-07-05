import re
from youtube_transcript_api import YouTubeTranscriptApi

def extract_youtube_url(text):
    """
    Extracts the first YouTube URL from a given string using regex.
    Supports standard and shortened youtu.be links.
    """
    # This regex looks for youtube.com/watch?v= or youtu.be/ links
    match = re.search(r'(https?://(?:www\.)?(?:youtube\.com/watch\?v=[\w-]+|youtu\.be/[\w-]+))', text)
    return match.group(1) if match else None

def get_video_id(url_link):
    """
    Extracts the video ID from a YouTube URL.
    """
    if "watch?v=" in url_link:
        return url_link.split("watch?v=")[-1].split('&')[0]
    elif "youtu.be/" in url_link:
        return url_link.split("youtu.be/")[-1].split('?')[0]
    return None

def get_transcript_from_url(url):
    """
    Retrieves the full transcript for a video from its URL.
    Returns the transcript as a single string or None if it fails.
    """
    try:
        video_id = get_video_id(url)
        if not video_id:
            return None
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([line['text'] for line in transcript_list])
    except Exception as e:
        print(f"Error retrieving transcript for {url}: {e}")
        return None