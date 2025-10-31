"""
Voice manager module
Manages voice selection and TTS settings
"""

from typing import Dict, Any, List, Optional
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class VoiceManager:
    """Manages voice profiles and TTS configuration"""
    
    # Available voice profiles (these would be actual Kyutai TTS voices)
    VOICES = {
        'default': {
            'id': 'default',
            'name': 'Default Voice',
            'language': 'en',
            'gender': 'neutral',
            'style': 'professional'
        },
        'energetic': {
            'id': 'energetic',
            'name': 'Energetic Voice',
            'language': 'en',
            'gender': 'neutral',
            'style': 'enthusiastic'
        },
        'calm': {
            'id': 'calm',
            'name': 'Calm Voice',
            'language': 'en',
            'gender': 'neutral',
            'style': 'soothing'
        },
        'authoritative': {
            'id': 'authoritative',
            'name': 'Authoritative Voice',
            'language': 'en',
            'gender': 'neutral',
            'style': 'confident'
        }
    }
    
    def __init__(self):
        """Initialize the VoiceManager"""
        self.current_voice = 'default'
    
    def get_voice(self, voice_id: str) -> Optional[Dict[str, Any]]:
        """
        Get voice profile by ID
        
        Args:
            voice_id: Voice identifier
            
        Returns:
            Voice profile dictionary or None if not found
        """
        if voice_id not in self.VOICES:
            logger.warning(f"Voice '{voice_id}' not found, using default")
            voice_id = 'default'
        
        return self.VOICES.get(voice_id)
    
    def list_voices(self) -> List[Dict[str, Any]]:
        """
        Get list of all available voices
        
        Returns:
            List of voice profile dictionaries
        """
        return list(self.VOICES.values())
    
    def set_voice(self, voice_id: str) -> bool:
        """
        Set the current voice
        
        Args:
            voice_id: Voice identifier
            
        Returns:
            True if successful, False otherwise
        """
        if voice_id in self.VOICES:
            self.current_voice = voice_id
            logger.info(f"Set voice to: {voice_id}")
            return True
        else:
            logger.error(f"Voice '{voice_id}' not found")
            return False
    
    def get_current_voice(self) -> Dict[str, Any]:
        """
        Get the current voice profile
        
        Returns:
            Current voice profile dictionary
        """
        return self.VOICES[self.current_voice]
    
    def recommend_voice(self, content_type: str) -> str:
        """
        Recommend a voice based on content type
        
        Args:
            content_type: Type of content (e.g., 'fact', 'story', 'tutorial')
            
        Returns:
            Recommended voice ID
        """
        recommendations = {
            'fact': 'authoritative',
            'story': 'energetic',
            'tutorial': 'calm',
            'entertainment': 'energetic',
            'education': 'professional'
        }
        
        voice_id = recommendations.get(content_type.lower(), 'default')
        logger.info(f"Recommended voice for '{content_type}': {voice_id}")
        return voice_id
    
    def get_voice_settings(self, voice_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get recommended TTS settings for a voice
        
        Args:
            voice_id: Voice identifier (uses current voice if not provided)
            
        Returns:
            Dictionary of TTS settings
        """
        if not voice_id:
            voice_id = self.current_voice
        
        voice = self.get_voice(voice_id)
        
        # Base settings
        settings = {
            'speed': 1.0,
            'pitch': 1.0,
            'volume': 1.0
        }
        
        # Adjust based on voice style
        if voice and voice.get('style') == 'enthusiastic':
            settings['speed'] = 1.1
            settings['pitch'] = 1.05
        elif voice and voice.get('style') == 'soothing':
            settings['speed'] = 0.95
        elif voice and voice.get('style') == 'confident':
            settings['pitch'] = 0.95
        
        return settings
    
    def validate_voice_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate voice configuration
        
        Args:
            config: Voice configuration dictionary
            
        Returns:
            True if valid, False otherwise
        """
        required_keys = ['speed', 'pitch', 'volume']
        
        if not all(key in config for key in required_keys):
            logger.error("Missing required keys in voice config")
            return False
        
        # Validate ranges
        if not (0.5 <= config['speed'] <= 2.0):
            logger.error("Speed must be between 0.5 and 2.0")
            return False
        
        if not (0.5 <= config['pitch'] <= 2.0):
            logger.error("Pitch must be between 0.5 and 2.0")
            return False
        
        if not (0.0 <= config['volume'] <= 2.0):
            logger.error("Volume must be between 0.0 and 2.0")
            return False
        
        return True
