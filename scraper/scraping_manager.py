import json
import os
from django.utils import timezone
from deals.models import EcommerceSite, Deal, DealCategory

class ScrapingManager:
    def __init__(self):
        # Load scraping configuration
        config_path = os.path.join(os.path.dirname(__file__), 'scraping_config.json')
        with open(config_path, 'r') as f:
            self.scraping_config = json.load(f)
        
    def run_scraping(self, test_mode=True):
        """Main scraping orchestration method"""
        print("=" * 50)
        print("STARTING DEAL SCRAPING")
        print("=" * 50)
        
        results = {}
        
        # Use test scraper for now
        from .site_scrapers import SimpleTestScraper
        scraper = SimpleTestScraper()
        
        deals_data = scraper.scrape_deals()
        
        if test_mode:
            print(f"\nFound {len(deals_data)} deals in test mode")
        
        # Process and save deals
        added_count = self.process_deals(deals_data, 'amazon')
        
        results['amazon'] = {
            'found': len(deals_data),
            'added': added_count
        }
        
        print("=" * 50)
        print("SCRAPING COMPLETED")
        print(f"Total deals added: {added_count}")
        print("=" * 50)
        
        return results
    
    def process_deals(self, deals_data, site_name):
        """Save deals to database"""
        added_count = 0
        
        # Get or create site object
        site_obj, created = EcommerceSite.objects.get_or_create(
            name=site_name,
            defaults={
                'base_url': 'amazon.com',
                'deals_page_url': 'https://www.amazon.com/gp/goldbox'
            }
        )
        
        print(f"\nProcessing deals for {site_name}...")
        
        for deal_data in deals_data:
            try:
                # Check if deal already exists
                existing_deal = Deal.objects.filter(deal_hash=deal_data['deal_hash']).first()
                
                if existing_deal:
                    print(f"Deal already exists: {deal_data['title'][:50]}...")
                    # Update existing deal
                    existing_deal.discounted_price = deal_data['discounted_price']
                    existing_deal.original_price = deal_data.get('original_price')
                    existing_deal.discount_percentage = deal_data['discount_percentage']
                    existing_deal.last_checked = timezone.now()
                    existing_deal.save()
                    continue
                
                # Get or create category
                category_name = deal_data.get('category', 'other')
                category_obj, _ = DealCategory.objects.get_or_create(
                    name=category_name,
                    defaults={'slug': category_name.lower().replace(' ', '-')}
                )
                
                # Calculate deal score
                deal_score = self.calculate_deal_score(deal_data)
                
                # Create new deal
                new_deal = Deal(
                    title=deal_data['title'][:200],
                    original_price=deal_data.get('original_price'),
                    discounted_price=deal_data['discounted_price'],
                    discount_percentage=deal_data['discount_percentage'],
                    product_url=deal_data['product_url'][:500],
                    image_url=deal_data.get('image_url', '')[:500],
                    source_site=site_obj,
                    category=category_obj,
                    deal_hash=deal_data['deal_hash'],
                    currency='USD',
                    is_active=True,
                    deal_score=deal_score
                )
                new_deal.save()
                
                print(f"✓ Added new deal: {deal_data['title'][:50]}...")
                added_count += 1
                
            except Exception as e:
                print(f"✗ Error saving deal: {e}")
                continue
        
        return added_count
    
    def calculate_deal_score(self, deal_data):
        """Calculate quality score for deal (0-100)"""
        score = 0
        
        # Higher discount = higher score
        discount = deal_data.get('discount_percentage', 0)
        score += min(60, discount * 0.6)
        
        # Amazon gets bonus points
        if deal_data.get('source') == 'amazon':
            score += 20
        
        # Price-based scoring
        price = deal_data.get('discounted_price', 0)
        if price < 50:
            score += 10
        elif price < 200:
            score += 5
        
        return min(100, int(score))