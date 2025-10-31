"""Unit tests for content sourcing module"""

import pytest
from viral_shorts.content_sourcing.fetchers import FactFetcher
from viral_shorts.content_sourcing.parsers import FactParser


def test_fact_parser():
    """Test fact parsing"""
    parser = FactParser()
    
    # Test valid fact
    fact_data = {'fact': 'The Earth is round.'}
    parsed = parser.parse_fact(fact_data)
    
    assert parsed is not None
    assert 'text' in parsed
    assert 'length' in parsed
    assert 'word_count' in parsed
    assert parsed['word_count'] == 4


def test_fact_validation():
    """Test fact validation"""
    parser = FactParser()
    
    # Valid fact
    valid_fact = {
        'text': 'This is a valid fact with enough words.',
        'word_count': 8,
        'length': 40
    }
    assert parser.validate_fact_for_video(valid_fact) == True
    
    # Too short
    short_fact = {
        'text': 'Too short',
        'word_count': 2,
        'length': 9
    }
    assert parser.validate_fact_for_video(short_fact) == False


def test_keyword_extraction():
    """Test keyword extraction"""
    parser = FactParser()
    
    text = "The Great Wall of China is one of the most impressive structures in the world."
    keywords = parser.extract_keywords(text)
    
    assert len(keywords) > 0
    assert 'Great' in keywords or 'Wall' in keywords or 'China' in keywords


if __name__ == '__main__':
    pytest.main([__file__])
