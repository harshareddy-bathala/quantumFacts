"""
YouTube publisher module
Handles video uploads to YouTube using the YouTube Data API v3
"""

import pickle
import os
from pathlib import Path
from typing import Optional, Dict, Any
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

from ..config import (
    YOUTUBE_CLIENT_SECRETS_FILE,
    YOUTUBE_OAUTH_TOKEN_FILE,
    YOUTUBE_CATEGORY_ID,
    YOUTUBE_PRIVACY_STATUS
)
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

# YouTube API scopes
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']


class YouTubePublisher:
    """Publishes videos to YouTube using the Data API v3"""
    
    def __init__(
        self,
        client_secrets_file: Optional[str] = None,
        token_file: Optional[str] = None
    ):
        """
        Initialize the YouTubePublisher
        
        Args:
            client_secrets_file: Path to OAuth client secrets JSON
            token_file: Path to store OAuth token
        """
        self.client_secrets_file = client_secrets_file or YOUTUBE_CLIENT_SECRETS_FILE
        self.token_file = token_file or YOUTUBE_OAUTH_TOKEN_FILE
        self.youtube = None
        self.credentials = None
    
    def authenticate(self) -> bool:
        """
        Authenticate with YouTube API using OAuth 2.0
        
        Returns:
            True if authentication successful, False otherwise
        """
        try:
            # Check if we have valid credentials
            if os.path.exists(self.token_file):
                with open(self.token_file, 'rb') as token:
                    self.credentials = pickle.load(token)
            
            # Refresh or get new credentials
            if not self.credentials or not self.credentials.valid:
                if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                    logger.info("Refreshing expired credentials...")
                    self.credentials.refresh(Request())
                else:
                    if not os.path.exists(self.client_secrets_file):
                        logger.error(
                            f"Client secrets file not found: {self.client_secrets_file}\n"
                            "Please download it from Google Cloud Console:\n"
                            "1. Go to https://console.cloud.google.com/\n"
                            "2. Enable YouTube Data API v3\n"
                            "3. Create OAuth 2.0 credentials\n"
                            "4. Download and save as 'client_secrets.json'"
                        )
                        return False
                    
                    logger.info("Starting OAuth flow...")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.client_secrets_file,
                        SCOPES
                    )
                    self.credentials = flow.run_local_server(port=0)
                
                # Save credentials for next time
                with open(self.token_file, 'wb') as token:
                    pickle.dump(self.credentials, token)
            
            # Build YouTube service
            self.youtube = build('youtube', 'v3', credentials=self.credentials)
            logger.info("Successfully authenticated with YouTube API")
            return True
            
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return False
    
    def upload_video(
        self,
        video_path: Path,
        title: str,
        description: str,
        tags: Optional[list] = None,
        category_id: Optional[int] = None,
        privacy_status: Optional[str] = None
    ) -> Optional[str]:
        """
        Upload a video to YouTube
        
        Args:
            video_path: Path to video file
            title: Video title
            description: Video description
            tags: List of tags
            category_id: YouTube category ID
            privacy_status: Privacy status (public, private, unlisted)
            
        Returns:
            Video ID if successful, None otherwise
        """
        try:
            if not self.youtube:
                if not self.authenticate():
                    logger.error("Failed to authenticate")
                    return None
            
            if not video_path.exists():
                logger.error(f"Video file not found: {video_path}")
                return None
            
            # Set defaults
            category_id = category_id or YOUTUBE_CATEGORY_ID
            privacy_status = privacy_status or YOUTUBE_PRIVACY_STATUS
            tags = tags or []
            
            # Prepare video metadata
            body = {
                'snippet': {
                    'title': title[:100],  # YouTube title limit
                    'description': description[:5000],  # YouTube description limit
                    'tags': tags[:500],  # YouTube allows up to 500 characters of tags
                    'categoryId': str(category_id)
                },
                'status': {
                    'privacyStatus': privacy_status,
                    'selfDeclaredMadeForKids': False
                }
            }
            
            # Create media upload
            media = MediaFileUpload(
                str(video_path),
                mimetype='video/*',
                resumable=True,
                chunksize=1024*1024  # 1MB chunks
            )
            
            logger.info(f"Uploading video: {title}")
            logger.info(f"Privacy status: {privacy_status}")
            
            # Execute upload
            request = self.youtube.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    logger.info(f"Upload progress: {progress}%")
            
            video_id = response.get('id')
            if video_id:
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                logger.info(f"Video uploaded successfully!")
                logger.info(f"Video ID: {video_id}")
                logger.info(f"Video URL: {video_url}")
                return video_id
            else:
                logger.error("Upload succeeded but no video ID returned")
                return None
                
        except HttpError as e:
            logger.error(f"YouTube API error: {e}")
            return None
        except Exception as e:
            logger.error(f"Error uploading video: {e}")
            return None
    
    def update_video_metadata(
        self,
        video_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[list] = None
    ) -> bool:
        """
        Update metadata of an existing video
        
        Args:
            video_id: YouTube video ID
            title: New title
            description: New description
            tags: New tags
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.youtube:
                if not self.authenticate():
                    return False
            
            # Get current video details
            response = self.youtube.videos().list(
                part='snippet',
                id=video_id
            ).execute()
            
            if not response.get('items'):
                logger.error(f"Video not found: {video_id}")
                return False
            
            snippet = response['items'][0]['snippet']
            
            # Update provided fields
            if title:
                snippet['title'] = title[:100]
            if description:
                snippet['description'] = description[:5000]
            if tags:
                snippet['tags'] = tags[:500]
            
            # Update video
            self.youtube.videos().update(
                part='snippet',
                body={
                    'id': video_id,
                    'snippet': snippet
                }
            ).execute()
            
            logger.info(f"Video metadata updated: {video_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating video metadata: {e}")
            return False
    
    def test_connection(self) -> bool:
        """
        Test if YouTube API connection is working
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            if not self.authenticate():
                return False
            
            # Try to get channel info
            response = self.youtube.channels().list(
                part='snippet',
                mine=True
            ).execute()
            
            if response.get('items'):
                channel_name = response['items'][0]['snippet']['title']
                logger.info(f"Connected to channel: {channel_name}")
                return True
            else:
                logger.error("No channel found")
                return False
                
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
