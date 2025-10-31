"""
Asset manager module
Handles downloading and managing video and audio assets
"""

import requests
import random
from pathlib import Path
from typing import Optional, List, Dict, Any
from ..config import (
    PEXELS_API_KEY,
    PIXABAY_API_KEY,
    PEXELS_API_URL,
    PIXABAY_API_URL,
    MUSIC_DIR,
    VIDEO_WIDTH,
    VIDEO_HEIGHT
)
from ..utils.logger import setup_logger
from ..utils.storage import StorageManager

logger = setup_logger(__name__)


class AssetManager:
    """Manages video and audio assets for video creation"""
    
    def __init__(
        self,
        pexels_key: Optional[str] = None,
        pixabay_key: Optional[str] = None
    ):
        """
        Initialize the AssetManager
        
        Args:
            pexels_key: Pexels API key (uses config if not provided)
            pixabay_key: Pixabay API key (uses config if not provided)
        """
        self.pexels_key = pexels_key or PEXELS_API_KEY
        self.pixabay_key = pixabay_key or PIXABAY_API_KEY
        self.storage = StorageManager()
        
        if not self.pexels_key and not self.pixabay_key:
            logger.warning(
                "No video API keys provided. Set PEXELS_API_KEY or "
                "PIXABAY_API_KEY in your .env file."
            )
    
    def search_pexels_videos(
        self,
        query: str,
        orientation: str = 'portrait',
        size: str = 'large',
        per_page: int = 15
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Search for videos on Pexels
        
        Args:
            query: Search query
            orientation: Video orientation (portrait, landscape, square)
            size: Video size (large, medium, small)
            per_page: Number of results per page
            
        Returns:
            List of video data dictionaries or None if failed
        """
        if not self.pexels_key:
            logger.error("Pexels API key not configured")
            return None
        
        try:
            headers = {
                'Authorization': self.pexels_key
            }
            
            params = {
                'query': query,
                'orientation': orientation,
                'size': size,
                'per_page': per_page
            }
            
            logger.info(f"Searching Pexels for: {query}")
            response = requests.get(
                PEXELS_API_URL,
                headers=headers,
                params=params,
                timeout=10
            )
            
            response.raise_for_status()
            data = response.json()
            
            videos = data.get('videos', [])
            logger.info(f"Found {len(videos)} videos on Pexels")
            return videos
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching Pexels: {e}")
            return None
    
    def search_pixabay_videos(
        self,
        query: str,
        video_type: str = 'film',
        per_page: int = 20
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Search for videos on Pixabay
        
        Args:
            query: Search query
            video_type: Type of video (all, film, animation)
            per_page: Number of results per page
            
        Returns:
            List of video data dictionaries or None if failed
        """
        if not self.pixabay_key:
            logger.error("Pixabay API key not configured")
            return None
        
        try:
            params = {
                'key': self.pixabay_key,
                'q': query,
                'video_type': video_type,
                'per_page': per_page
            }
            
            logger.info(f"Searching Pixabay for: {query}")
            response = requests.get(
                PIXABAY_API_URL,
                params=params,
                timeout=10
            )
            
            response.raise_for_status()
            data = response.json()
            
            videos = data.get('hits', [])
            logger.info(f"Found {len(videos)} videos on Pixabay")
            return videos
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching Pixabay: {e}")
            return None
    
    def download_video(
        self,
        video_url: str,
        output_dir: Optional[Path] = None,
        filename: Optional[str] = None,
        max_retries: int = 3
    ) -> Optional[Path]:
        """
        Download a video from URL with retry logic
        
        Args:
            video_url: URL of the video to download
            output_dir: Directory to save video
            filename: Custom filename (auto-generated if not provided)
            max_retries: Maximum number of download attempts
            
        Returns:
            Path to downloaded video or None if failed
        """
        import time
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Downloading video from: {video_url} (attempt {attempt + 1}/{max_retries})")
                
                # Stream download with chunks to handle large files
                response = requests.get(
                    video_url, 
                    stream=True, 
                    timeout=60,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                response.raise_for_status()
                
                if not filename:
                    filename = f"background.mp4"
                
                if not output_dir:
                    output_dir = Path('.')
                
                file_path = output_dir / filename
                
                # Download in chunks with progress
                total_size = int(response.headers.get('content-length', 0))
                chunk_size = 8192
                downloaded = 0
                
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            # Log progress every 5MB
                            if downloaded % (5 * 1024 * 1024) < chunk_size:
                                progress = (downloaded / total_size * 100) if total_size > 0 else 0
                                logger.debug(f"Downloaded: {downloaded / (1024*1024):.1f}MB ({progress:.1f}%)")
                
                logger.info(f"Video downloaded: {file_path}")
                return file_path
                
            except (requests.exceptions.RequestException, IOError) as e:
                logger.warning(f"Download attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                    logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Error downloading video after {max_retries} attempts: {e}")
                    return None
        
        return None
    
    def find_best_video(
        self,
        keywords: List[str],
        source: str = 'both',
        min_duration: int = 10
    ) -> Optional[Dict[str, Any]]:
        """
        Find the best matching video from multiple sources
        
        Args:
            keywords: List of search keywords
            source: Video source ('pexels', 'pixabay', or 'both')
            min_duration: Minimum video duration in seconds
            
        Returns:
            Best video data dictionary or None if not found
        """
        all_videos = []
        
        # Try each keyword
        for keyword in keywords[:3]:  # Limit to first 3 keywords
            if source in ['pexels', 'both'] and self.pexels_key:
                pexels_videos = self.search_pexels_videos(keyword)
                if pexels_videos:
                    # Filter videos by duration
                    filtered = [
                        v for v in pexels_videos 
                        if v.get('duration', 0) >= min_duration and v.get('video_files')
                    ]
                    all_videos.extend([
                        {
                            'source': 'pexels',
                            'data': video,
                            'keyword': keyword,
                            'duration': video.get('duration', 0)
                        }
                        for video in filtered
                    ])
            
            if source in ['pixabay', 'both'] and self.pixabay_key:
                pixabay_videos = self.search_pixabay_videos(keyword)
                if pixabay_videos:
                    # Filter videos by duration
                    filtered = [
                        v for v in pixabay_videos 
                        if v.get('duration', 0) >= min_duration and v.get('videos')
                    ]
                    all_videos.extend([
                        {
                            'source': 'pixabay',
                            'data': video,
                            'keyword': keyword,
                            'duration': video.get('duration', 0)
                        }
                        for video in filtered
                    ])
        
        if not all_videos:
            logger.warning("No videos found with sufficient duration")
            return None
        
        # Prefer videos with longer duration
        all_videos.sort(key=lambda x: x.get('duration', 0), reverse=True)
        
        # Select from top 5 videos randomly
        top_videos = all_videos[:5]
        selected = random.choice(top_videos)
        logger.info(f"Selected {selected['duration']}s video from {selected['source']} for keyword: {selected['keyword']}")
        
        return selected
    
    def get_video_url(self, video_data: Dict[str, Any]) -> Optional[str]:
        """
        Extract the video URL from API response data
        
        Args:
            video_data: Video data from find_best_video
            
        Returns:
            Video URL or None if not found
        """
        try:
            source = video_data.get('source')
            data = video_data.get('data', {})
            
            if source == 'pexels':
                # Find the best quality portrait video
                video_files = data.get('video_files', [])
                portrait_files = [
                    f for f in video_files
                    if f.get('width', 0) < f.get('height', 0)  # Portrait orientation
                ]
                
                if portrait_files:
                    # Sort by quality and get highest
                    best_file = max(portrait_files, key=lambda x: x.get('width', 0))
                    return best_file.get('link')
            
            elif source == 'pixabay':
                # Get medium quality video for faster downloads (still good quality)
                videos = data.get('videos', {})
                # Prefer medium quality to avoid large file downloads
                for quality in ['medium', 'large', 'small']:
                    video_info = videos.get(quality)
                    if video_info:
                        return video_info.get('url')
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting video URL: {e}")
            return None
    
    def get_background_music(self) -> Optional[Path]:
        """
        Get a random background music file from the music directory
        
        Returns:
            Path to music file or None if not found
        """
        try:
            # Find all audio files in music directory
            audio_files = []
            for ext in ['.mp3', '.wav', '.ogg', '.m4a']:
                audio_files.extend(MUSIC_DIR.glob(f'*{ext}'))
            
            if not audio_files:
                logger.warning(f"No music files found in {MUSIC_DIR}")
                return None
            
            # Select random file
            music_file = random.choice(audio_files)
            logger.info(f"Selected background music: {music_file.name}")
            return music_file
            
        except Exception as e:
            logger.error(f"Error getting background music: {e}")
            return None
    
    def test_apis(self) -> Dict[str, bool]:
        """
        Test if video APIs are accessible
        
        Returns:
            Dictionary with API test results
        """
        results = {}
        
        if self.pexels_key:
            videos = self.search_pexels_videos('nature', per_page=1)
            results['pexels'] = videos is not None
        else:
            results['pexels'] = False
        
        if self.pixabay_key:
            videos = self.search_pixabay_videos('nature', per_page=1)
            results['pixabay'] = videos is not None
        else:
            results['pixabay'] = False
        
        return results
