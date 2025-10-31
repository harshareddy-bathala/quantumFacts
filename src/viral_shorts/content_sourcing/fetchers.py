"""
Fact fetcher module
Retrieves interesting facts from API-Ninjas Facts API
"""

import requests
from typing import Optional, Dict, Any
from ..config import API_NINJAS_KEY, API_NINJAS_FACTS_URL
from ..utils.logger import setup_logger

logger = setup_logger(__name__)


class FactFetcher:
    """Fetches random interesting facts from API-Ninjas"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the FactFetcher
        
        Args:
            api_key: API-Ninjas API key (uses config if not provided)
        """
        self.api_key = api_key or API_NINJAS_KEY
        self.base_url = API_NINJAS_FACTS_URL
        
        if not self.api_key:
            raise ValueError("API_NINJAS_KEY is required. Set it in your .env file.")
    
    def fetch_random_fact(self, limit: int = 1) -> Optional[Dict[str, Any]]:
        """
        Fetch a random fact from the API
        
        Args:
            limit: Number of facts to fetch (default: 1)
            
        Returns:
            Dictionary containing the fact data or None if failed
        """
        try:
            headers = {
                'X-Api-Key': self.api_key
            }
            
            # Note: limit parameter is premium only, so we don't use it
            params = {}
            
            logger.info(f"Fetching random fact from API-Ninjas...")
            response = requests.get(
                self.base_url,
                headers=headers,
                params=params,
                timeout=10
            )
            
            response.raise_for_status()
            data = response.json()
            
            if data and len(data) > 0:
                logger.info(f"Successfully fetched fact: {data[0]['fact'][:50]}...")
                return data[0] if limit == 1 else data
            else:
                logger.error("No facts returned from API")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching fact from API: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return None
    
    def fetch_fact_by_category(self, category: str) -> Optional[Dict[str, Any]]:
        """
        Fetch a fact from a specific category (if supported in future)
        
        Args:
            category: Category of fact to fetch
            
        Returns:
            Dictionary containing the fact data or None if failed
        """
        # Note: API-Ninjas Facts API doesn't currently support categories
        # This method is a placeholder for future functionality
        logger.warning("Category filtering not yet supported by API-Ninjas Facts API")
        return self.fetch_random_fact()
    
    def test_connection(self) -> bool:
        """
        Test if the API connection is working
        
        Returns:
            True if connection is successful, False otherwise
        """
        try:
            result = self.fetch_random_fact()
            return result is not None
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
