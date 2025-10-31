"""
Script generator module
Uses OpenRouter API to generate video scripts from facts
"""

import json
import requests
from typing import Dict, Any, Optional
from ..config import (
    OPENROUTER_API_KEY,
    OPENROUTER_API_URL,
    OPENROUTER_MODEL,
    OPENROUTER_MAX_TOKENS,
    OPENROUTER_TEMPERATURE
)
from ..utils.logger import setup_logger
from .prompts import PromptTemplates

logger = setup_logger(__name__)


class ScriptGenerator:
    """Generates video scripts using OpenRouter LLM API"""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the ScriptGenerator
        
        Args:
            api_key: OpenRouter API key (uses config if not provided)
            model: Model to use (uses config if not provided)
        """
        self.api_key = api_key or OPENROUTER_API_KEY
        self.model = model or OPENROUTER_MODEL
        self.base_url = OPENROUTER_API_URL
        
        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY is required. Set it in your .env file.")
    
    def _call_llm(self, prompt: str, max_tokens: int = OPENROUTER_MAX_TOKENS) -> Optional[str]:
        """
        Call the OpenRouter API
        
        Args:
            prompt: The prompt to send
            max_tokens: Maximum tokens in response
            
        Returns:
            The response text or None if failed
        """
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json',
                'HTTP-Referer': 'https://github.com/viral-shorts-generator',
                'X-Title': 'Viral Shorts Generator'
            }
            
            payload = {
                'model': self.model,
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'max_tokens': max_tokens,
                'temperature': OPENROUTER_TEMPERATURE
            }
            
            logger.info(f"Calling OpenRouter API with model: {self.model}")
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            data = response.json()
            
            if 'choices' in data and len(data['choices']) > 0:
                content = data['choices'][0]['message']['content']
                logger.info("Successfully received response from OpenRouter")
                return content
            else:
                logger.error("No choices in API response")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling OpenRouter API: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None
    
    def generate_script(self, fact: str) -> Optional[Dict[str, Any]]:
        """
        Generate a complete video script from a fact
        
        Args:
            fact: The fact to base the script on
            
        Returns:
            Dictionary containing script, title, description, etc.
        """
        try:
            prompt = PromptTemplates.format_script_prompt(fact)
            response = self._call_llm(prompt)
            
            if not response:
                logger.error("Failed to generate script")
                return None
            
            # Try to parse JSON response
            try:
                # Extract JSON from response (in case it's wrapped in markdown)
                if '```json' in response:
                    response = response.split('```json')[1].split('```')[0].strip()
                elif '```' in response:
                    response = response.split('```')[1].split('```')[0].strip()
                
                script_data = json.loads(response)
                
                # Validate required fields
                required_fields = ['hook', 'script', 'title', 'description']
                if not all(field in script_data for field in required_fields):
                    logger.error("Script data missing required fields")
                    return None
                
                logger.info(f"Generated script with title: {script_data['title']}")
                return script_data
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON response: {e}")
                logger.debug(f"Response was: {response}")
                
                # Fallback: create basic structure
                return {
                    'hook': fact[:100],
                    'script': fact,
                    'title': f"Amazing Fact: {fact[:40]}...",
                    'description': f"{fact}\n\n#facts #interesting #shorts",
                    'hashtags': ['facts', 'interesting', 'shorts', 'viral', 'amazing'],
                    'keywords': ['fact', 'interesting', 'amazing']
                }
                
        except Exception as e:
            logger.error(f"Error generating script: {e}")
            return None
    
    def optimize_title(self, title: str) -> Optional[list]:
        """
        Generate alternative optimized titles
        
        Args:
            title: Original title
            
        Returns:
            List of alternative titles or None if failed
        """
        try:
            prompt = PromptTemplates.format_title_prompt(title)
            response = self._call_llm(prompt, max_tokens=200)
            
            if not response:
                return None
            
            # Parse JSON response
            if '```json' in response:
                response = response.split('```json')[1].split('```')[0].strip()
            
            data = json.loads(response)
            return data.get('titles', [])
            
        except Exception as e:
            logger.error(f"Error optimizing title: {e}")
            return None
    
    def generate_hashtags(self, topic: str, keywords: list) -> Optional[list]:
        """
        Generate relevant hashtags
        
        Args:
            topic: Main topic
            keywords: List of keywords
            
        Returns:
            List of hashtags or None if failed
        """
        try:
            prompt = PromptTemplates.format_hashtag_prompt(topic, keywords)
            response = self._call_llm(prompt, max_tokens=300)
            
            if not response:
                return None
            
            # Parse JSON response
            if '```json' in response:
                response = response.split('```json')[1].split('```')[0].strip()
            
            data = json.loads(response)
            return data.get('hashtags', [])
            
        except Exception as e:
            logger.error(f"Error generating hashtags: {e}")
            return None
    
    def test_connection(self) -> bool:
        """
        Test if the API connection is working
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            response = self._call_llm("Say 'Hello'", max_tokens=10)
            return response is not None
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
