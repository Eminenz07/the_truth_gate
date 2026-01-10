from django import template
import re
from urllib.parse import urlparse, parse_qs

register = template.Library()

@register.filter
def youtube_embed(url):
    """
    Convert a YouTube URL to an embed URL.
    Handles:
    - youtube.com/watch?v=VIDEO_ID
    - youtu.be/VIDEO_ID
    - Already formatted embed URLs
    """
    if not url:
        return url
    
    # Already an embed URL
    if '/embed/' in url:
        return url
    
    # Extract video ID from various YouTube URL formats
    video_id = None
    
    # Pattern 1: youtube.com/watch?v=VIDEO_ID
    if 'youtube.com/watch' in url:
        parsed = urlparse(url)
        video_id = parse_qs(parsed.query).get('v', [None])[0]
    
    # Pattern 2: youtu.be/VIDEO_ID
    elif 'youtu.be/' in url:
        video_id = url.split('youtu.be/')[-1].split('?')[0]
    
    # Pattern 3: youtube.com/live/VIDEO_ID
    elif 'youtube.com/live/' in url:
        video_id = url.split('/live/')[-1].split('?')[0]
    
    if video_id:
        return f'https://www.youtube.com/embed/{video_id}'
    
    # Return original URL if we couldn't parse it
    return url
