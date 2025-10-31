"""
Main orchestration script for the Viral YouTube Shorts Generator
Coordinates all modules to create and publish videos
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

from .config import validate_config, get_config_summary, OUTPUT_DIR, AUTO_PUBLISH
from .utils.logger import setup_logger
from .utils.storage import StorageManager
from .content_sourcing.fetchers import FactFetcher
from .content_sourcing.parsers import FactParser
from .scripting.script_generator import ScriptGenerator
from .narration.tts import KyutaiTTS
from .narration.voice_manager import VoiceManager
from .video_assembly.assets import AssetManager
from .video_assembly.editor import VideoEditor
from .publishing.youtube_publisher import YouTubePublisher
from .publishing.scheduler import VideoScheduler

logger = setup_logger(__name__)


class ViralShortsGenerator:
    """Main orchestrator for automated viral shorts generation"""
    
    def __init__(self):
        """Initialize the generator"""
        logger.info("Initializing Viral Shorts Generator...")
        
        # Validate configuration
        try:
            validate_config()
            logger.info("Configuration validated successfully")
        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            raise
        
        # Initialize modules
        self.fact_fetcher = FactFetcher()
        self.fact_parser = FactParser()
        self.script_generator = ScriptGenerator()
        self.tts = KyutaiTTS()
        self.voice_manager = VoiceManager()
        self.asset_manager = AssetManager()
        self.video_editor = VideoEditor()
        self.youtube_publisher = YouTubePublisher()
        self.scheduler = VideoScheduler()
        self.storage = StorageManager()
        
        logger.info("All modules initialized successfully")
    
    def generate_video(self, publish: bool = False) -> Optional[Dict[str, Any]]:
        """
        Generate a complete video from scratch
        
        Args:
            publish: Whether to publish to YouTube immediately
            
        Returns:
            Dictionary with video information or None if failed
        """
        try:
            logger.info("=" * 80)
            logger.info("Starting video generation pipeline...")
            logger.info("=" * 80)
            
            # Step 1: Fetch a random fact
            logger.info("\n[1/7] Fetching random fact...")
            fact_data = self.fact_fetcher.fetch_random_fact()
            if not fact_data:
                logger.error("Failed to fetch fact")
                return None
            
            # Step 2: Parse and validate fact
            logger.info("\n[2/7] Parsing fact...")
            parsed_fact = self.fact_parser.parse_fact(fact_data)
            if not parsed_fact:
                logger.error("Failed to parse fact")
                return None
            
            fact_text = parsed_fact['text']
            logger.info(f"Fact: {fact_text}")
            
            # Step 3: Generate script
            logger.info("\n[3/7] Generating script with AI...")
            script_data = self.script_generator.generate_script(fact_text)
            if not script_data:
                logger.error("Failed to generate script")
                return None
            
            logger.info(f"Title: {script_data['title']}")
            logger.info(f"Script: {script_data['script'][:100]}...")
            
            # Step 4: Generate narration
            logger.info("\n[4/7] Generating narration (TTS)...")
            full_script = f"{script_data['hook']} {script_data['script']}"
            
            # Create video directory
            video_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            video_dir = self.storage.create_video_directory(video_id)
            
            # Generate speech
            voice_id = self.voice_manager.recommend_voice('fact')
            narration_path = video_dir / 'narration.wav'
            
            tts_result = self.tts.generate_speech(
                full_script,
                narration_path,
                voice=voice_id
            )
            
            if not tts_result:
                logger.error("Failed to generate narration")
                return None
            
            word_timestamps = tts_result['word_timestamps']
            audio_duration = tts_result['duration']
            logger.info(f"Narration generated: {audio_duration:.2f} seconds")
            
            # Step 5: Find and download background video
            logger.info("\n[5/7] Finding background video...")
            keywords = self.fact_parser.extract_keywords(fact_text)
            logger.info(f"Search keywords: {', '.join(keywords)}")
            
            # Try up to 3 different videos if download fails
            background_video = None
            max_video_attempts = 3
            
            for attempt in range(max_video_attempts):
                video_data = self.asset_manager.find_best_video(keywords)
                if not video_data:
                    logger.error("Failed to find background video")
                    return None
                
                video_url = self.asset_manager.get_video_url(video_data)
                if not video_url:
                    logger.warning("Failed to get video URL, trying another video...")
                    continue
                
                background_video = self.asset_manager.download_video(
                    video_url,
                    video_dir,
                    'background.mp4'
                )
                
                if background_video:
                    logger.info(f"Background video downloaded")
                    break
                else:
                    logger.warning(f"Download failed (attempt {attempt + 1}/{max_video_attempts}), trying another video...")
            
            if not background_video:
                logger.error("Failed to download video after multiple attempts")
                return None
            
            # Step 6: Get background music
            logger.info("\n[6/7] Getting background music...")
            background_music = self.asset_manager.get_background_music()
            if background_music:
                logger.info(f"Music: {background_music.name}")
            else:
                logger.warning("No background music available")
            
            # Step 7: Assemble final video
            logger.info("\n[7/7] Assembling final video...")
            output_path = video_dir / f"{video_id}.mp4"
            
            final_video = self.video_editor.create_complete_video(
                background_video=background_video,
                voice_audio=Path(tts_result['audio_path']),
                background_music=background_music,
                word_timestamps=word_timestamps,
                output_path=output_path,
                target_duration=audio_duration
            )
            
            if not final_video:
                logger.error("Failed to assemble video")
                return None
            
            logger.info(f"Video created successfully: {final_video}")
            
            # Prepare video information
            video_info = {
                'video_id': video_id,
                'video_path': str(final_video),
                'title': script_data['title'],
                'description': script_data['description'],
                'hashtags': script_data.get('hashtags', []),
                'fact': fact_text,
                'duration': audio_duration,
                'created_at': datetime.now().isoformat()
            }
            
            # Save video metadata
            metadata_file = video_dir / 'metadata.json'
            import json
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(video_info, f, indent=2)
            
            logger.info("=" * 80)
            logger.info("Video generation completed successfully!")
            logger.info("=" * 80)
            
            # Publish if requested
            if publish or AUTO_PUBLISH:
                logger.info("\nPublishing to YouTube...")
                youtube_id = self.publish_video(video_info)
                if youtube_id:
                    video_info['youtube_id'] = youtube_id
                    logger.info(f"Published to YouTube: {youtube_id}")
            
            return video_info
            
        except Exception as e:
            logger.error(f"Error in video generation pipeline: {e}", exc_info=True)
            return None
    
    def publish_video(self, video_info: Dict[str, Any]) -> Optional[str]:
        """
        Publish a video to YouTube
        
        Args:
            video_info: Video information dictionary
            
        Returns:
            YouTube video ID or None if failed
        """
        try:
            video_path = Path(video_info['video_path'])
            
            # Combine hashtags into description
            hashtags = video_info.get('hashtags', [])
            description = video_info['description']
            if hashtags:
                description += '\n\n' + ' '.join(f'#{tag}' for tag in hashtags)
            
            # Upload to YouTube
            youtube_id = self.youtube_publisher.upload_video(
                video_path=video_path,
                title=video_info['title'],
                description=description,
                tags=hashtags
            )
            
            return youtube_id
            
        except Exception as e:
            logger.error(f"Error publishing video: {e}")
            return None
    
    def test_apis(self) -> Dict[str, bool]:
        """
        Test all API connections
        
        Returns:
            Dictionary with test results for each API
        """
        logger.info("Testing API connections...")
        
        results = {
            'fact_api': self.fact_fetcher.test_connection(),
            'script_generator': self.script_generator.test_connection(),
            'tts': self.tts.test_connection(),
            'video_apis': self.asset_manager.test_apis(),
            'youtube': self.youtube_publisher.test_connection()
        }
        
        # Print results
        logger.info("\nAPI Test Results:")
        for api, status in results.items():
            status_str = "✓ PASS" if status else "✗ FAIL"
            logger.info(f"  {api}: {status_str}")
        
        return results
    
    def show_config(self):
        """Display current configuration"""
        config = get_config_summary()
        logger.info("\nCurrent Configuration:")
        for key, value in config.items():
            logger.info(f"  {key}: {value}")


def main():
    """Main entry point"""
    try:
        # Create generator instance
        generator = ViralShortsGenerator()
        
        # Show configuration
        generator.show_config()
        
        # Test APIs (optional, comment out to skip)
        logger.info("\nTesting API connections...")
        generator.test_apis()
        
        # Generate a video
        logger.info("\nGenerating video...")
        video_info = generator.generate_video(publish=False)
        
        if video_info:
            logger.info("\n" + "=" * 80)
            logger.info("SUCCESS!")
            logger.info(f"Video saved to: {video_info['video_path']}")
            logger.info(f"Title: {video_info['title']}")
            logger.info("=" * 80)
            return 0
        else:
            logger.error("\nVideo generation failed")
            return 1
            
    except KeyboardInterrupt:
        logger.info("\nOperation cancelled by user")
        return 130
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
