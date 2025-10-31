"""Unit tests for publishing module"""

import pytest
from pathlib import Path
from viral_shorts.publishing.scheduler import VideoScheduler


def test_scheduler_queue():
    """Test video scheduler queue operations"""
    scheduler = VideoScheduler()
    
    # Add to queue
    result = scheduler.add_to_queue(
        video_path=Path('test.mp4'),
        title='Test Video',
        description='Test Description',
        tags=['test', 'video']
    )
    
    assert result == True
    
    # Get stats
    stats = scheduler.get_queue_stats()
    assert stats['total'] > 0


if __name__ == '__main__':
    pytest.main([__file__])
