"""
Video URL Parser - Multi-Platform Support
Supports YouTube, Dailymotion, Vimeo, TikTok, Twitch, and 1000+ sites via yt-dlp
"""

import re
from urllib.parse import urlparse
import yt_dlp


class VideoParser:
    """Parse and extract video information from multiple platforms"""
    
    SUPPORTED_PLATFORMS = {
        'youtube.com': 'YouTube',
        'youtu.be': 'YouTube',
        'dailymotion.com': 'Dailymotion',
        'dai.ly': 'Dailymotion',
        'vimeo.com': 'Vimeo',
        'tiktok.com': 'TikTok',
        'twitch.tv': 'Twitch',
        'facebook.com': 'Facebook',
        'instagram.com': 'Instagram',
        'twitter.com': 'Twitter',
        'x.com': 'Twitter',
    }
    
    @staticmethod
    def detect_platform(url):
        """Detect which platform a URL belongs to"""
        try:
            domain = urlparse(url).netloc.replace('www.', '').replace('m.', '')
            for platform_domain, platform_name in VideoParser.SUPPORTED_PLATFORMS.items():
                if platform_domain in domain:
                    return platform_name
            return 'Other'  # Unknown but might still be supported by yt-dlp
        except Exception:
            return None
    
    @staticmethod
    def extract_metadata(url):
        """Extract video metadata using yt-dlp"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'skip_download': True,
            'no_check_certificate': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Get best thumbnail
                thumbnail = None
                if info.get('thumbnail'):
                    thumbnail = info.get('thumbnail')
                elif info.get('thumbnails') and len(info.get('thumbnails')) > 0:
                    thumbnail = info['thumbnails'][-1].get('url')
                
                return {
                    'title': info.get('title', 'Untitled Video'),
                    'description': (info.get('description', '') or '')[:500],
                    'thumbnail': thumbnail,
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'platform': VideoParser.detect_platform(url),
                    'success': True
                }
        except Exception as e:
            # Fallback: basic info from URL
            platform = VideoParser.detect_platform(url)
            return {
                'title': url.split('/')[-1][:100] or 'Untitled Video',
                'description': f'Video from {platform}' if platform else 'Saved video',
                'thumbnail': None,
                'duration': 0,
                'uploader': 'Unknown',
                'platform': platform,
                'success': False,
                'error': str(e)
            }
    
    @staticmethod
    def is_valid_video_url(url):
        """Validate if URL is from a supported video platform"""
        if not url or len(url) < 10:
            return False
        
        # Basic URL validation
        try:
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                return False
        except Exception:
            return False
        
        # Check if it's a known platform or let yt-dlp try
        platform = VideoParser.detect_platform(url)
        return platform is not None
    
    @staticmethod
    def format_duration(seconds):
        """Format duration in seconds to HH:MM:SS or MM:SS"""
        if not seconds or seconds == 0:
            return "00:00"
        
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
