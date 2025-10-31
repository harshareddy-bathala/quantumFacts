"""
Configuration management for the Viral Shorts Generator
Loads settings from environment variables and provides defaults
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base Directories
BASE_DIR = Path(__file__).parent.parent.parent
OUTPUT_DIR = Path(os.getenv('OUTPUT_DIR', BASE_DIR / 'output'))
ASSETS_DIR = Path(os.getenv('ASSETS_DIR', BASE_DIR / 'assets'))
MUSIC_DIR = Path(os.getenv('MUSIC_DIR', ASSETS_DIR / 'music'))
TEMP_DIR = Path(os.getenv('TEMP_DIR', BASE_DIR / 'temp'))

# Create directories if they don't exist
for directory in [OUTPUT_DIR, ASSETS_DIR, MUSIC_DIR, TEMP_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# API Keys
API_NINJAS_KEY = os.getenv('API_NINJAS_KEY', '')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY', '')
PEXELS_API_KEY = os.getenv('PEXELS_API_KEY', '')
PIXABAY_API_KEY = os.getenv('PIXABAY_API_KEY', '')

# API Endpoints
API_NINJAS_FACTS_URL = "https://api.api-ninjas.com/v1/facts"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
PEXELS_API_URL = "https://api.pexels.com/videos/search"
PIXABAY_API_URL = "https://pixabay.com/api/videos"

# Google Colab Configuration
COLAB_NOTEBOOK_URL = os.getenv('COLAB_NOTEBOOK_URL', '')

# YouTube Configuration
YOUTUBE_CLIENT_SECRETS_FILE = os.getenv('YOUTUBE_CLIENT_SECRETS_FILE', str(BASE_DIR / 'client_secrets.json'))
YOUTUBE_OAUTH_TOKEN_FILE = os.getenv('YOUTUBE_OAUTH_TOKEN_FILE', str(BASE_DIR / 'oauth_token.json'))
YOUTUBE_CATEGORY_ID = int(os.getenv('YOUTUBE_CATEGORY_ID', '28'))  # Science & Technology
YOUTUBE_PRIVACY_STATUS = os.getenv('YOUTUBE_PRIVACY_STATUS', 'public')
AUTO_PUBLISH = os.getenv('AUTO_PUBLISH', 'false').lower() == 'true'

# Video Settings
VIDEO_WIDTH = int(os.getenv('VIDEO_WIDTH', '1080'))
VIDEO_HEIGHT = int(os.getenv('VIDEO_HEIGHT', '1920'))
VIDEO_FPS = int(os.getenv('VIDEO_FPS', '30'))
VIDEO_DURATION_MAX = int(os.getenv('VIDEO_DURATION_MAX', '60'))
VIDEO_FORMAT = 'mp4'
VIDEO_CODEC = 'libx264'
VIDEO_PRESET = 'medium'

# Audio Settings
BACKGROUND_MUSIC_VOLUME = float(os.getenv('BACKGROUND_MUSIC_VOLUME', '0.2'))
VOICE_VOLUME = float(os.getenv('VOICE_VOLUME', '1.0'))
AUDIO_CODEC = 'aac'
AUDIO_BITRATE = '192k'

# Subtitle Settings - Professional YouTube Shorts Style
SUBTITLE_FONT = 'Arial'  # Clean, professional font
SUBTITLE_FONT_SIZE = 24  # Smaller, cleaner size
SUBTITLE_COLOR = '&H00FFFF&'  # Yellow (like popular shorts) - BGR format
SUBTITLE_OUTLINE_COLOR = '&H000000&'  # Black
SUBTITLE_OUTLINE = 2  # Medium outline for readability
SUBTITLE_BOLD = True
SUBTITLE_SHADOW = 0  # No shadow for cleaner look
SUBTITLE_POSITION = 2  # Bottom center (2 = bottom)
SUBTITLE_MARGIN_V = 150  # More margin from bottom in pixels

# Content Settings
FACTS_CATEGORY = os.getenv('FACTS_CATEGORY', 'random')
VIDEO_LANGUAGE = os.getenv('VIDEO_LANGUAGE', 'en')

# OpenRouter Model Settings
# Using a free model - check https://openrouter.ai/models for current free models
OPENROUTER_MODEL = os.getenv('OPENROUTER_MODEL', 'mistralai/mistral-7b-instruct:free')  # Free tier model
OPENROUTER_MAX_TOKENS = 1000
OPENROUTER_TEMPERATURE = 0.7

# FFmpeg Settings
FFMPEG_COMMAND = 'ffmpeg'
FFMPEG_LOGLEVEL = 'error'

# Logging Settings
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = BASE_DIR / 'logs' / 'viral_shorts.log'

# Create logs directory
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


def validate_config():
    """
    Validate that all required configuration values are set
    Raises ValueError if critical configuration is missing
    """
    required_keys = {
        'API_NINJAS_KEY': API_NINJAS_KEY,
        'OPENROUTER_API_KEY': OPENROUTER_API_KEY,
    }
    
    missing_keys = [key for key, value in required_keys.items() if not value]
    
    if missing_keys:
        raise ValueError(
            f"Missing required configuration: {', '.join(missing_keys)}. "
            f"Please set these in your .env file."
        )
    
    return True


def get_config_summary():
    """Return a dictionary with current configuration (excluding sensitive data)"""
    return {
        'output_dir': str(OUTPUT_DIR),
        'assets_dir': str(ASSETS_DIR),
        'video_dimensions': f"{VIDEO_WIDTH}x{VIDEO_HEIGHT}",
        'video_fps': VIDEO_FPS,
        'max_duration': VIDEO_DURATION_MAX,
        'openrouter_model': OPENROUTER_MODEL,
        'youtube_category': YOUTUBE_CATEGORY_ID,
        'auto_publish': AUTO_PUBLISH,
    }
