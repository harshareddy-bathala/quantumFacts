"""
Storage manager module
Handles file storage, cleanup, and organization
"""

import shutil
from pathlib import Path
from typing import List, Optional
from datetime import datetime, timedelta
from ..config import OUTPUT_DIR, TEMP_DIR, ASSETS_DIR
from .logger import setup_logger

logger = setup_logger(__name__)


class StorageManager:
    """Manages file storage and cleanup for the application"""
    
    def __init__(self):
        """Initialize the StorageManager"""
        self.output_dir = OUTPUT_DIR
        self.temp_dir = TEMP_DIR
        self.assets_dir = ASSETS_DIR
        
        # Ensure directories exist
        for directory in [self.output_dir, self.temp_dir, self.assets_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def create_video_directory(self, video_id: Optional[str] = None) -> Path:
        """
        Create a directory for a specific video
        
        Args:
            video_id: Unique video identifier (uses timestamp if not provided)
            
        Returns:
            Path to the created directory
        """
        if not video_id:
            video_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        video_dir = self.output_dir / video_id
        video_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Created video directory: {video_dir}")
        return video_dir
    
    def save_file(self, content: bytes, filename: str, directory: Optional[Path] = None) -> Optional[Path]:
        """
        Save content to a file
        
        Args:
            content: File content as bytes
            filename: Name of the file
            directory: Directory to save in (uses temp_dir if not provided)
            
        Returns:
            Path to saved file or None if failed
        """
        try:
            save_dir = directory or self.temp_dir
            save_dir.mkdir(parents=True, exist_ok=True)
            
            file_path = save_dir / filename
            
            with open(file_path, 'wb') as f:
                f.write(content)
            
            logger.info(f"Saved file: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            return None
    
    def copy_file(self, source: Path, destination: Path) -> bool:
        """
        Copy a file from source to destination
        
        Args:
            source: Source file path
            destination: Destination file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
            logger.info(f"Copied file from {source} to {destination}")
            return True
        except Exception as e:
            logger.error(f"Error copying file: {e}")
            return False
    
    def move_file(self, source: Path, destination: Path) -> bool:
        """
        Move a file from source to destination
        
        Args:
            source: Source file path
            destination: Destination file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(destination))
            logger.info(f"Moved file from {source} to {destination}")
            return True
        except Exception as e:
            logger.error(f"Error moving file: {e}")
            return False
    
    def delete_file(self, file_path: Path) -> bool:
        """
        Delete a file
        
        Args:
            file_path: Path to file to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if file_path.exists():
                file_path.unlink()
                logger.info(f"Deleted file: {file_path}")
                return True
            else:
                logger.warning(f"File not found: {file_path}")
                return False
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            return False
    
    def clean_temp_directory(self, older_than_hours: int = 24) -> int:
        """
        Clean temporary files older than specified hours
        
        Args:
            older_than_hours: Delete files older than this many hours
            
        Returns:
            Number of files deleted
        """
        try:
            deleted_count = 0
            cutoff_time = datetime.now() - timedelta(hours=older_than_hours)
            
            for file_path in self.temp_dir.glob('**/*'):
                if file_path.is_file():
                    file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if file_time < cutoff_time:
                        file_path.unlink()
                        deleted_count += 1
            
            logger.info(f"Cleaned {deleted_count} temporary files")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Error cleaning temp directory: {e}")
            return 0
    
    def get_storage_stats(self) -> dict:
        """
        Get storage statistics
        
        Returns:
            Dictionary with storage information
        """
        def get_dir_size(path: Path) -> int:
            """Calculate total size of directory"""
            total = 0
            try:
                for file_path in path.glob('**/*'):
                    if file_path.is_file():
                        total += file_path.stat().st_size
            except Exception as e:
                logger.error(f"Error calculating directory size: {e}")
            return total
        
        return {
            'output_dir': {
                'path': str(self.output_dir),
                'size_mb': round(get_dir_size(self.output_dir) / (1024 * 1024), 2),
                'files': len(list(self.output_dir.glob('**/*')))
            },
            'temp_dir': {
                'path': str(self.temp_dir),
                'size_mb': round(get_dir_size(self.temp_dir) / (1024 * 1024), 2),
                'files': len(list(self.temp_dir.glob('**/*')))
            },
            'assets_dir': {
                'path': str(self.assets_dir),
                'size_mb': round(get_dir_size(self.assets_dir) / (1024 * 1024), 2),
                'files': len(list(self.assets_dir.glob('**/*')))
            }
        }
    
    def list_videos(self) -> List[Path]:
        """
        List all video files in output directory
        
        Returns:
            List of video file paths
        """
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
        videos = []
        
        for ext in video_extensions:
            videos.extend(self.output_dir.glob(f'**/*{ext}'))
        
        return sorted(videos, key=lambda x: x.stat().st_mtime, reverse=True)
