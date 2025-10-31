"""
Video scheduler module
Handles scheduling and queuing of video uploads
"""

import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from ..utils.logger import setup_logger
from ..utils.storage import StorageManager

logger = setup_logger(__name__)


class VideoScheduler:
    """Manages video upload scheduling and queue"""
    
    def __init__(self, queue_file: Optional[Path] = None):
        """
        Initialize the VideoScheduler
        
        Args:
            queue_file: Path to queue file (auto-created if not provided)
        """
        self.storage = StorageManager()
        self.queue_file = queue_file or (self.storage.output_dir / 'upload_queue.json')
        self.queue = self._load_queue()
    
    def _load_queue(self) -> List[Dict[str, Any]]:
        """Load upload queue from file"""
        try:
            if self.queue_file.exists():
                with open(self.queue_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error loading queue: {e}")
            return []
    
    def _save_queue(self) -> bool:
        """Save upload queue to file"""
        try:
            with open(self.queue_file, 'w', encoding='utf-8') as f:
                json.dump(self.queue, f, indent=2, default=str)
            return True
        except Exception as e:
            logger.error(f"Error saving queue: {e}")
            return False
    
    def add_to_queue(
        self,
        video_path: Path,
        title: str,
        description: str,
        tags: List[str],
        scheduled_time: Optional[datetime] = None
    ) -> bool:
        """
        Add a video to the upload queue
        
        Args:
            video_path: Path to video file
            title: Video title
            description: Video description
            tags: List of tags
            scheduled_time: When to upload (immediate if not provided)
            
        Returns:
            True if added successfully, False otherwise
        """
        try:
            video_info = {
                'id': str(int(time.time() * 1000)),
                'video_path': str(video_path),
                'title': title,
                'description': description,
                'tags': tags,
                'scheduled_time': scheduled_time or datetime.now(),
                'status': 'pending',
                'added_at': datetime.now()
            }
            
            self.queue.append(video_info)
            self._save_queue()
            
            logger.info(f"Added video to queue: {title}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding to queue: {e}")
            return False
    
    def get_pending_uploads(self) -> List[Dict[str, Any]]:
        """
        Get videos that are ready to be uploaded
        
        Returns:
            List of video info dictionaries
        """
        now = datetime.now()
        pending = []
        
        for video in self.queue:
            if video['status'] == 'pending':
                scheduled = video.get('scheduled_time')
                if isinstance(scheduled, str):
                    scheduled = datetime.fromisoformat(scheduled)
                
                if scheduled <= now:
                    pending.append(video)
        
        return pending
    
    def mark_uploaded(self, video_id: str, youtube_id: str) -> bool:
        """
        Mark a video as uploaded
        
        Args:
            video_id: Queue video ID
            youtube_id: YouTube video ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            for video in self.queue:
                if video['id'] == video_id:
                    video['status'] = 'uploaded'
                    video['youtube_id'] = youtube_id
                    video['uploaded_at'] = datetime.now()
                    self._save_queue()
                    logger.info(f"Marked video as uploaded: {video_id}")
                    return True
            
            logger.error(f"Video not found in queue: {video_id}")
            return False
            
        except Exception as e:
            logger.error(f"Error marking as uploaded: {e}")
            return False
    
    def mark_failed(self, video_id: str, error: str) -> bool:
        """
        Mark a video upload as failed
        
        Args:
            video_id: Queue video ID
            error: Error message
            
        Returns:
            True if successful, False otherwise
        """
        try:
            for video in self.queue:
                if video['id'] == video_id:
                    video['status'] = 'failed'
                    video['error'] = error
                    video['failed_at'] = datetime.now()
                    self._save_queue()
                    logger.info(f"Marked video as failed: {video_id}")
                    return True
            
            logger.error(f"Video not found in queue: {video_id}")
            return False
            
        except Exception as e:
            logger.error(f"Error marking as failed: {e}")
            return False
    
    def schedule_batch(
        self,
        videos: List[Dict[str, Any]],
        interval_hours: int = 2
    ) -> bool:
        """
        Schedule multiple videos with intervals between them
        
        Args:
            videos: List of video info dictionaries
            interval_hours: Hours between each upload
            
        Returns:
            True if successful, False otherwise
        """
        try:
            current_time = datetime.now()
            
            for i, video in enumerate(videos):
                scheduled_time = current_time + timedelta(hours=i * interval_hours)
                self.add_to_queue(
                    Path(video['video_path']),
                    video['title'],
                    video['description'],
                    video['tags'],
                    scheduled_time
                )
            
            logger.info(f"Scheduled {len(videos)} videos with {interval_hours}h intervals")
            return True
            
        except Exception as e:
            logger.error(f"Error scheduling batch: {e}")
            return False
    
    def get_queue_stats(self) -> Dict[str, int]:
        """
        Get statistics about the upload queue
        
        Returns:
            Dictionary with queue statistics
        """
        stats = {
            'total': len(self.queue),
            'pending': 0,
            'uploaded': 0,
            'failed': 0
        }
        
        for video in self.queue:
            status = video.get('status', 'pending')
            if status in stats:
                stats[status] += 1
        
        return stats
    
    def clear_completed(self, older_than_days: int = 7) -> int:
        """
        Remove completed uploads older than specified days
        
        Args:
            older_than_days: Remove uploads older than this many days
            
        Returns:
            Number of entries removed
        """
        try:
            cutoff = datetime.now() - timedelta(days=older_than_days)
            original_count = len(self.queue)
            
            self.queue = [
                video for video in self.queue
                if not (
                    video['status'] == 'uploaded' and
                    datetime.fromisoformat(str(video.get('uploaded_at', datetime.now()))) < cutoff
                )
            ]
            
            removed = original_count - len(self.queue)
            if removed > 0:
                self._save_queue()
                logger.info(f"Cleared {removed} completed uploads")
            
            return removed
            
        except Exception as e:
            logger.error(f"Error clearing completed: {e}")
            return 0
