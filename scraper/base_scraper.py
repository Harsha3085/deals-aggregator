import requests
from bs4 import BeautifulSoup
import time
import json
import logging
from urllib.parse import urljoin
import re

logger = logging.getLogger(__name__)

class BaseScraper:
    def __init__(self, site_config):
        self.site_config = site_config
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def get_page(self, url):
        """Fetch page with retry logic"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                return response.text
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
        return None
    
    def parse_price(self, price_text):
        """Extract numeric price from text"""
        if not price_text:
            return None
        # Remove currency symbols and commas
        price_str = re.sub(r'[^\d.]', '', price_text)
        try:
            return float(price_str)
        except:
            return None
    
    def calculate_discount(self, original, discounted):
        """Calculate discount percentage"""
        if original and discounted and original > 0:
            return int(((original - discounted) / original) * 100)
        return 0
    
    def create_deal_hash(self, deal_data):
        """Create unique hash for deal"""
        import hashlib
        hash_string = f"{deal_data['title']}_{deal_data['source']}_{deal_data['discounted_price']}"
        return hashlib.sha256(hash_string.encode()).hexdigest()
    
    def categorize_deal(self, title):
        """Simple categorization based on keywords"""
        title_lower = title.lower()
        
        categories = {
            'electronics': ['phone', 'laptop', 'tablet', 'earphone', 'headphone', 'charger', 'camera', 'smartwatch', 'tv'],
            'fashion': ['shirt', 'dress', 'shoe', 'jeans', 'jacket', 'watch', 'bag', 'jewelry', 'sunglass'],
            'home': ['kitchen', 'furniture', 'decor', 'light', 'bed', 'sofa', 'mat', 'cookware'],
            'books': ['book', 'novel', 'kindle'],
            'sports': ['sport', 'fitness', 'gym', 'yoga', 'cycle']
        }
        
        for category, keywords in categories.items():
            if any(keyword in title_lower for keyword in keywords):
                return category
        
        return 'other'
    