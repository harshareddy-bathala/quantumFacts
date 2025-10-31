"""
Video editor module
Handles FFmpeg-based video assembly, audio mixing, and subtitle generation
"""

import subprocess
import pysubs2
from pathlib import Path
from typing import Optional, List, Dict, Any
from ..config import (
    VIDEO_WIDTH,
    VIDEO_HEIGHT,
    VIDEO_FPS,
    VIDEO_CODEC,
    VIDEO_PRESET,
    AUDIO_CODEC,
    AUDIO_BITRATE,
    BACKGROUND_MUSIC_VOLUME,
    VOICE_VOLUME,
    SUBTITLE_FONT,
    SUBTITLE_FONT_SIZE,
    SUBTITLE_COLOR,
    SUBTITLE_OUTLINE_COLOR,
    SUBTITLE_OUTLINE,
    SUBTITLE_BOLD,
    SUBTITLE_SHADOW,
    SUBTITLE_POSITION,
    SUBTITLE_MARGIN_V,
    FFMPEG_COMMAND,
    FFMPEG_LOGLEVEL,
    TEMP_DIR
)
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class VideoEditor:
    """Assembles final video using FFmpeg"""
    
    def __init__(self):
        """Initialize the VideoEditor"""
        self.ffmpeg_cmd = FFMPEG_COMMAND
        self._test_ffmpeg()
    
    def _test_ffmpeg(self) -> bool:
        """Test if FFmpeg is available"""
        try:
            result = subprocess.run(
                [self.ffmpeg_cmd, '-version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                logger.info("FFmpeg is available")
                return True
            else:
                logger.error("FFmpeg test failed")
                return False
        except Exception as e:
            logger.error(f"FFmpeg not found: {e}")
            logger.warning(
                "Please install FFmpeg: https://ffmpeg.org/download.html"
            )
            return False
    
    def create_animated_subtitles(
        self,
        word_timestamps: List[Dict[str, Any]],
        output_path: Optional[Path] = None
    ) -> Optional[Path]:
        """
        Create animated word-by-word subtitles in ASS format
        
        Args:
            word_timestamps: List of word timestamp dictionaries
            output_path: Path to save subtitle file
            
        Returns:
            Path to subtitle file or None if failed
        """
        try:
            if not output_path:
                output_path = TEMP_DIR / 'subtitles.ass'
            
            # Create ASS subtitle file
            subs = pysubs2.SSAFile()
            
            # Configure style - Professional YouTube Shorts look
            style = pysubs2.SSAStyle()
            style.fontname = SUBTITLE_FONT
            style.fontsize = SUBTITLE_FONT_SIZE
            style.primarycolor = pysubs2.Color(0, 255, 255)  # Yellow (RGB in pysubs2)
            style.outlinecolor = pysubs2.Color(0, 0, 0)  # Black outline
            style.outline = SUBTITLE_OUTLINE
            style.shadow = SUBTITLE_SHADOW
            style.bold = SUBTITLE_BOLD
            # Alignment: 1=left-bottom, 2=center-bottom, 3=right-bottom, 5=left-top, etc.
            style.alignment = 2  # Bottom center
            style.marginv = SUBTITLE_MARGIN_V  # Bottom margin in pixels
            
            # Add slight uppercase for better readability (optional)
            # This can be applied to individual words if needed
            
            subs.styles["Default"] = style
            
            # Add each word as a separate event with uppercase for impact
            for word_data in word_timestamps:
                word = word_data['word']
                start_ms = int(word_data['start'] * 1000)
                end_ms = int(word_data['end'] * 1000)
                
                # Make words uppercase for better readability (like viral shorts)
                word_display = word.upper()
                
                event = pysubs2.SSAEvent(
                    start=start_ms,
                    end=end_ms,
                    text=word_display
                )
                subs.append(event)
            
            # Save the subtitle file
            subs.save(str(output_path))
            logger.info(f"Created animated subtitles: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating subtitles: {e}")
            return None
    
    def mix_audio(
        self,
        voice_path: Path,
        music_path: Optional[Path],
        output_path: Optional[Path] = None,
        voice_volume: float = VOICE_VOLUME,
        music_volume: float = BACKGROUND_MUSIC_VOLUME
    ) -> Optional[Path]:
        """
        Mix voice and background music
        
        Args:
            voice_path: Path to voice audio file
            music_path: Path to background music file
            output_path: Path to save mixed audio
            voice_volume: Voice volume multiplier
            music_volume: Music volume multiplier
            
        Returns:
            Path to mixed audio file or None if failed
        """
        try:
            if not output_path:
                output_path = TEMP_DIR / 'mixed_audio.aac'
            
            if not music_path or not music_path.exists():
                # No music, just use voice
                logger.info("No background music, using voice only")
                return voice_path
            
            # FFmpeg command to mix audio
            cmd = [
                self.ffmpeg_cmd,
                '-i', str(voice_path),
                '-i', str(music_path),
                '-filter_complex',
                f'[0:a]volume={voice_volume}[a1];[1:a]volume={music_volume}[a2];[a1][a2]amix=inputs=2:duration=first',
                '-c:a', AUDIO_CODEC,
                '-b:a', AUDIO_BITRATE,
                '-loglevel', FFMPEG_LOGLEVEL,
                '-y',  # Overwrite output
                str(output_path)
            ]
            
            logger.info("Mixing audio tracks...")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                logger.info(f"Audio mixed successfully: {output_path}")
                return output_path
            else:
                logger.error(f"Audio mixing failed: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"Error mixing audio: {e}")
            return None
    
    def assemble_video(
        self,
        video_path: Path,
        audio_path: Path,
        subtitle_path: Optional[Path],
        output_path: Path,
        duration: Optional[float] = None
    ) -> Optional[Path]:
        """
        Assemble final video with video, audio, and subtitles
        
        Args:
            video_path: Path to background video
            audio_path: Path to audio file
            subtitle_path: Path to subtitle file
            output_path: Path to save final video
            duration: Video duration in seconds (trims video if specified)
            
        Returns:
            Path to final video or None if failed
        """
        try:
            # Build FFmpeg command with stream_loop for better video quality
            cmd = [
                self.ffmpeg_cmd,
                '-stream_loop', '-1',  # Loop video indefinitely
                '-i', str(video_path),
                '-i', str(audio_path),
            ]
            
            # Build filter complex
            filters = []
            
            # Scale and crop video to portrait format - video will play continuously
            filters.append(
                f'[0:v]scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=increase,'
                f'crop={VIDEO_WIDTH}:{VIDEO_HEIGHT}[v]'
            )
            
            # Add subtitles if provided
            if subtitle_path and subtitle_path.exists():
                # Escape the path for FFmpeg
                sub_path_escaped = str(subtitle_path).replace('\\', '/').replace(':', '\\:')
                filters.append(f'[v]ass={sub_path_escaped}[vout]')
                video_label = '[vout]'
            else:
                video_label = '[v]'
            
            # Add filter complex to command
            cmd.extend([
                '-filter_complex', ';'.join(filters),
                '-map', video_label,
                '-map', '1:a',
            ])
            
            # Add duration if specified
            if duration:
                cmd.extend(['-t', str(duration)])
            
            # Video encoding settings
            cmd.extend([
                '-c:v', VIDEO_CODEC,
                '-preset', VIDEO_PRESET,
                '-c:a', AUDIO_CODEC,
                '-b:a', AUDIO_BITRATE,
                '-r', str(VIDEO_FPS),
                '-pix_fmt', 'yuv420p',  # Compatibility
                '-loglevel', FFMPEG_LOGLEVEL,
                '-y',  # Overwrite output
                str(output_path)
            ])
            
            logger.info("Assembling final video...")
            logger.debug(f"FFmpeg command: {' '.join(cmd)}")
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                logger.info(f"Video assembled successfully: {output_path}")
                return output_path
            else:
                logger.error(f"Video assembly failed: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            logger.error("Video assembly timed out")
            return None
        except Exception as e:
            logger.error(f"Error assembling video: {e}")
            return None
    
    def get_video_duration(self, video_path: Path) -> Optional[float]:
        """
        Get duration of a video file in seconds
        
        Args:
            video_path: Path to video file
            
        Returns:
            Duration in seconds or None if failed
        """
        try:
            cmd = [
                'ffprobe',
                '-v', 'error',
                '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                str(video_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                duration = float(result.stdout.strip())
                return duration
            else:
                logger.error("Failed to get video duration")
                return None
                
        except Exception as e:
            logger.error(f"Error getting video duration: {e}")
            return None
    
    def create_complete_video(
        self,
        background_video: Path,
        voice_audio: Path,
        background_music: Optional[Path],
        word_timestamps: List[Dict[str, Any]],
        output_path: Path,
        target_duration: Optional[float] = None
    ) -> Optional[Path]:
        """
        Complete video creation pipeline
        
        Args:
            background_video: Path to background video
            voice_audio: Path to voice narration
            background_music: Path to background music (optional)
            word_timestamps: Word-level timestamps for subtitles
            output_path: Path to save final video
            target_duration: Target video duration
            
        Returns:
            Path to final video or None if failed
        """
        try:
            logger.info("Starting complete video creation pipeline...")
            
            # Step 1: Create subtitles
            subtitle_path = self.create_animated_subtitles(word_timestamps)
            if not subtitle_path:
                logger.warning("Failed to create subtitles, continuing without them")
                subtitle_path = None
            
            # Step 2: Mix audio
            mixed_audio = self.mix_audio(voice_audio, background_music)
            if not mixed_audio:
                logger.error("Failed to mix audio")
                return None
            
            # Step 3: Assemble video
            final_video = self.assemble_video(
                background_video,
                mixed_audio,
                subtitle_path,
                output_path,
                duration=target_duration
            )
            
            if final_video:
                logger.info("Video creation pipeline completed successfully!")
            
            return final_video
            
        except Exception as e:
            logger.error(f"Error in video creation pipeline: {e}")
            return None
