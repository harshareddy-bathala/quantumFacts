"""Narration module for text-to-speech conversion"""

from .tts import KyutaiTTS
from .voice_manager import VoiceManager

__all__ = ['KyutaiTTS', 'VoiceManager']
