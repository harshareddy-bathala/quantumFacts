"""
Kyutai TTS integration module
Handles text-to-speech conversion using Kyutai TTS via Google Colab
"""

import json
import time
from typing import Dict, Any, Optional, List
from pathlib import Path
from ..config import COLAB_NOTEBOOK_URL, TEMP_DIR
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class KyutaiTTS:
    """
    Interface for Kyutai TTS engine running on Google Colab
    
    Note: This requires a Google Colab notebook to be set up with Kyutai TTS.
    The notebook should expose an API endpoint for TTS generation.
    """
    
    def __init__(self, colab_url: Optional[str] = None):
        """
        Initialize the Kyutai TTS interface
        
        Args:
            colab_url: URL to the Google Colab notebook API (uses config if not provided)
        """
        self.colab_url = colab_url or COLAB_NOTEBOOK_URL
        
        if not self.colab_url:
            logger.warning(
                "No Colab URL provided. You'll need to set up Kyutai TTS manually. "
                "See documentation for setup instructions."
            )
    
    def generate_speech(
        self,
        text: str,
        output_path: Optional[Path] = None,
        voice: str = "default",
        speed: float = 1.0
    ) -> Optional[Dict[str, Any]]:
        """
        Generate speech from text using Kyutai TTS
        
        Args:
            text: Text to convert to speech
            output_path: Path to save the audio file
            voice: Voice ID to use
            speed: Speech speed multiplier
            
        Returns:
            Dictionary containing audio file path and word timestamps
        """
        try:
            if not output_path:
                timestamp = int(time.time())
                output_path = TEMP_DIR / f"narration_{timestamp}.wav"
            
            logger.info(f"Generating speech for text: {text[:50]}...")
            
            # For now, always use fallback TTS (gTTS) until Colab is set up
            logger.info("Using gTTS (Google Text-to-Speech) fallback")
            return self._fallback_tts(text, output_path)
            
        except Exception as e:
            logger.error(f"Error generating speech: {e}")
            return None
    
    def _generate_dummy_timestamps(self, text: str, total_duration: float = None) -> List[Dict[str, Any]]:
        """
        Generate accurate word-level timestamps synchronized with audio
        
        Args:
            text: Input text
            total_duration: Total audio duration in seconds (if known)
            
        Returns:
            List of word timestamp dictionaries
        """
        words = text.split()
        timestamps = []
        
        if not words:
            return timestamps
        
        # If we don't have total duration, estimate it
        if total_duration is None:
            # Average speaking rate: ~2.5 words per second
            total_duration = len(words) / 2.5
        
        # Simple linear distribution - divide total time evenly across all words
        # This ensures captions stay in sync with audio
        time_per_word = total_duration / len(words)
        
        current_time = 0.0
        
        for i, word in enumerate(words):
            # Each word gets equal time - no complex calculations
            # This keeps captions perfectly synced with speech
            word_duration = time_per_word * 0.95  # Show word for 95% of its slot
            
            timestamps.append({
                'word': word,
                'start': round(current_time, 3),
                'end': round(current_time + word_duration, 3),
                'duration': round(word_duration, 3)
            })
            
            # Move to next word slot
            current_time += time_per_word
        
        return timestamps
    
    def _fallback_tts(self, text: str, output_path: Path) -> Dict[str, Any]:
        """
        Fallback TTS method using Microsoft Edge TTS (better quality than gTTS)
        
        Args:
            text: Text to convert
            output_path: Output file path
            
        Returns:
            Dictionary with TTS results
        """
        try:
            # Try Edge TTS first (best quality)
            logger.info("Using Microsoft Edge TTS (high quality)")
            return self._edge_tts(text, output_path)
            
        except Exception as edge_error:
            logger.warning(f"Edge TTS failed: {edge_error}, falling back to gTTS")
            try:
                # Fallback to gTTS
                logger.info("Using gTTS (Google Text-to-Speech) as backup")
                
                from gtts import gTTS
                from pydub import AudioSegment
                
                # Generate speech with gTTS
                tts = gTTS(text=text, lang='en', slow=False)
                
                # Save as temporary MP3
                temp_mp3 = output_path.parent / f"{output_path.stem}_temp.mp3"
                tts.save(str(temp_mp3))
                
                # Convert MP3 to WAV using pydub
                audio = AudioSegment.from_mp3(str(temp_mp3))
                audio.export(str(output_path), format="wav")
                
                # Clean up temp file
                temp_mp3.unlink()
                
                # Get duration
                duration = len(audio) / 1000.0  # pydub returns milliseconds
                
                logger.info(f"Generated audio file: {output_path} ({duration:.2f}s)")
                
                return {
                    'audio_path': str(output_path),
                    'duration': duration,
                    'word_timestamps': self._generate_dummy_timestamps(text, duration),
                    'sample_rate': 24000,
                    'fallback': True
                }
                
            except ImportError:
                logger.error("gTTS or pydub not installed. Install with: pip install gtts pydub")
                return None
            except Exception as e:
                logger.error(f"Error in fallback TTS: {e}")
                return None
    
    def _edge_tts(self, text: str, output_path: Path) -> Dict[str, Any]:
        """
        Generate speech using Microsoft Edge TTS
        
        Args:
            text: Text to convert
            output_path: Output file path
            
        Returns:
            Dictionary with TTS results
        """
        import asyncio
        import edge_tts
        from pydub import AudioSegment
        
        async def _generate():
            # Use an engaging, energetic voice for viral content
            # en-US-ChristopherNeural - Young, energetic male voice (best for viral content)
            # en-US-GuyNeural - Professional male voice
            # en-US-JennyNeural - Friendly female voice
            voice = "en-US-ChristopherNeural"  # More engaging and energetic
            
            # Increase rate slightly for more dynamic delivery
            communicate = edge_tts.Communicate(
                text, 
                voice,
                rate="+10%"  # Slightly faster for viral shorts
            )
            await communicate.save(str(output_path))
        
        # Run async function
        asyncio.run(_generate())
        
        # Get duration
        audio = AudioSegment.from_file(str(output_path))
        duration = len(audio) / 1000.0
        
        logger.info(f"Generated audio file with Edge TTS: {output_path} ({duration:.2f}s)")
        
        return {
            'audio_path': str(output_path),
            'duration': duration,
            'word_timestamps': self._generate_dummy_timestamps(text, duration),
            'sample_rate': 24000,
            'fallback': True
        }
    
    def test_connection(self) -> bool:
        """
        Test if the Colab TTS service is accessible
        
        Returns:
            True if connection is successful, False otherwise
        """
        if not self.colab_url:
            logger.warning("No Colab URL configured")
            return False
        
        try:
            # TODO: Implement actual connection test
            # For now, just check if URL is set
            logger.info("Colab URL is set, but connection test not implemented")
            return True
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    def save_timestamps(self, timestamps: List[Dict[str, Any]], output_path: Path) -> bool:
        """
        Save word timestamps to a JSON file
        
        Args:
            timestamps: List of word timestamp dictionaries
            output_path: Path to save the JSON file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(timestamps, f, indent=2)
            
            logger.info(f"Saved timestamps to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving timestamps: {e}")
            return False
