"""
Fact parser module
Processes and validates fact data for video generation
"""

from typing import Dict, Any, Optional
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class FactParser:
    """Parses and validates fact data from API responses"""
    
    @staticmethod
    def parse_fact(fact_data: Dict[str, Any]) -> Optional[Dict[str, str]]:
        """
        Parse fact data from API response
        
        Args:
            fact_data: Raw fact data from API
            
        Returns:
            Parsed fact dictionary or None if invalid
        """
        try:
            if not fact_data:
                logger.error("No fact data provided")
                return None
            
            # Extract the fact text
            fact_text = fact_data.get('fact', '')
            
            if not fact_text:
                logger.error("Fact text is empty")
                return None
            
            # Basic validation
            if len(fact_text) < 10:
                logger.warning("Fact is too short (less than 10 characters)")
                return None
            
            if len(fact_text) > 500:
                logger.warning("Fact is very long, may need trimming")
            
            parsed = {
                'text': fact_text,
                'length': len(fact_text),
                'word_count': len(fact_text.split())
            }
            
            logger.info(f"Parsed fact: {parsed['word_count']} words, {parsed['length']} characters")
            return parsed
            
        except Exception as e:
            logger.error(f"Error parsing fact: {e}")
            return None
    
    @staticmethod
    def validate_fact_for_video(fact: Dict[str, str], max_words: int = 100) -> bool:
        """
        Validate if a fact is suitable for a short video
        
        Args:
            fact: Parsed fact dictionary
            max_words: Maximum word count for video (default: 100)
            
        Returns:
            True if fact is suitable, False otherwise
        """
        try:
            word_count = fact.get('word_count', 0)
            
            if word_count == 0:
                logger.error("Fact has no words")
                return False
            
            if word_count < 5:
                logger.warning("Fact is too short (less than 5 words)")
                return False
            
            if word_count > max_words:
                logger.warning(f"Fact is too long ({word_count} > {max_words} words)")
                return False
            
            logger.info("Fact is suitable for video")
            return True
            
        except Exception as e:
            logger.error(f"Error validating fact: {e}")
            return False
    
    @staticmethod
    def clean_fact_text(text: str) -> str:
        """
        Clean and normalize fact text
        
        Args:
            text: Raw fact text
            
        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Ensure proper ending punctuation
        if not text.endswith(('.', '!', '?')):
            text += '.'
        
        return text
    
    @staticmethod
    def extract_keywords(fact_text: str, max_keywords: int = 3) -> list:
        """
        Extract keywords from fact text for video search
        
        Args:
            fact_text: Fact text
            max_keywords: Maximum number of keywords (default: 3)
            
        Returns:
            List of keywords
        """
        # Remove common words (expanded list)
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'can', 'that', 'this', 'these',
            'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'their', 'them',
            'over', 'years', 'year', 'however', 'because', 'only', 'also', 'when',
            'made', 'make', 'used', 'than'
        }
        
        # Priority words that are good for video search (proper nouns, specific objects)
        priority_indicators = ['pyramid', 'ocean', 'mountain', 'space', 'animal', 'city',
                             'country', 'planet', 'star', 'galaxy', 'earth', 'sun', 'moon']
        
        # Split into words and filter
        words = fact_text.lower().split()
        keywords = []
        priority_keywords = []
        
        for word in words:
            clean_word = word.strip('.,!?;:()[]{}"\'-')
            # Skip if too short or is a stop word
            if len(clean_word) < 4 or clean_word.lower() in stop_words:
                continue
            # Check if it's a priority word
            if any(indicator in clean_word for indicator in priority_indicators):
                if clean_word not in priority_keywords:
                    priority_keywords.append(clean_word)
            elif clean_word not in keywords:
                keywords.append(clean_word)
        
        # Combine priority keywords first, then regular keywords
        final_keywords = priority_keywords + keywords
        
        # If we have too few keywords, add generic fallback topics
        if len(final_keywords) < 2:
            final_keywords.extend(['nature', 'science', 'discovery'])
        
        # Return top keywords (limit to max_keywords)
        return final_keywords[:max_keywords]
