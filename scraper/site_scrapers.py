from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class AmazonScraper(BaseScraper):
    def scrape_deals(self):
        url = self.site_config.get('deals_page')
        print(f"Scraping Amazon deals from: {url}")
        
        html = self.get_page(url)
        
        if not html:
            print("Failed to fetch Amazon page")
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        selectors = self.site_config.get('selectors', {})
        
        deals = []
        # Let's look for deal containers
        deal_containers = soup.select(selectors.get('deal_container', ''))
        
        print(f"Found {len(deal_containers)} deal containers")
        
        # If no containers found with that selector, try a different approach
        if len(deal_containers) == 0:
            # Try alternative selectors
            deal_containers = soup.find_all('div', {'data-component-type': 's-search-result'})
            print(f"Trying alternative: found {len(deal_containers)} containers")
        
        for container in deal_containers[:10]:  # Limit to 10 for testing
            try:
                # Try multiple selectors for title
                title = None
                title_selectors = [
                    selectors.get('title', ''),
                    'h2 a span',  # Alternative
                    '.a-text-normal',  # Alternative
                ]
                
                for selector in title_selectors:
                    if selector:
                        title_elem = container.select_one(selector)
                        if title_elem:
                            title = title_elem.get_text(strip=True)
                            break
                
                if not title:
                    continue
                
                # Try to find price
                price_selectors = [
                    selectors.get('price_discounted', ''),
                    '.a-price-whole',  # Alternative
                    '.a-offscreen',  # Alternative
                ]
                
                price_text = None
                for selector in price_selectors:
                    if selector:
                        price_elem = container.select_one(selector)
                        if price_elem:
                            price_text = price_elem.get_text(strip=True)
                            break
                
                if not price_text:
                    continue
                
                discounted_price = self.parse_price(price_text)
                
                if not discounted_price:
                    continue
                
                # Try to find original price
                original_price = None
                original_selectors = [
                    selectors.get('price_original', ''),
                    '.a-text-price span',  # Alternative
                ]
                
                for selector in original_selectors:
                    if selector:
                        original_elem = container.select_one(selector)
                        if original_elem:
                            original_text = original_elem.get_text(strip=True)
                            original_price = self.parse_price(original_text)
                            if original_price:
                                break
                
                # Find product link
                link_elem = container.select_one('a')
                product_url = ''
                if link_elem and link_elem.get('href'):
                    product_url = urljoin(url, link_elem.get('href'))
                
                # Find image
                image_elem = container.select_one('img')
                image_url = ''
                if image_elem:
                    image_url = image_elem.get('src', '')
                    if not image_url:
                        image_url = image_elem.get('data-src', '')
                
                # Calculate discount
                discount_percentage = self.calculate_discount(original_price, discounted_price)
                
                # Create deal
                deal = {
                    'title': title[:200],
                    'original_price': original_price,
                    'discounted_price': discounted_price,
                    'discount_percentage': discount_percentage,
                    'product_url': product_url[:500],
                    'image_url': image_url[:500],
                    'source': 'amazon',
                    'category': self.categorize_deal(title),
                    'deal_hash': self.create_deal_hash({
                        'title': title,
                        'source': 'amazon',
                        'discounted_price': discounted_price
                    })
                }
                
                print(f"Found deal: {title[:50]}... - ${discounted_price}")
                deals.append(deal)
                
            except Exception as e:
                print(f"Error parsing deal: {e}")
                continue
        
        print(f"Total deals found: {len(deals)}")
        return deals

# Simple test scraper for demo
class SimpleTestScraper:
    def scrape_deals(self):
        """Return test data for demonstration"""
        print("Using test scraper (demo mode)")
        
        test_deals = [
            {
                'title': 'Wireless Bluetooth Headphones - Noise Cancelling',
                'original_price': 99.99,
                'discounted_price': 59.99,
                'discount_percentage': 40,
                'product_url': 'https://www.amazon.com/demo-product-1',
                'image_url': 'https://m.media-amazon.com/images/I/71an9eiBxpL._AC_SL1500_.jpg',
                'source': 'amazon',
                'category': 'electronics',
                'deal_hash': 'test_hash_1'
            },
            {
                'title': 'Men\'s Running Shoes - Comfort & Style',
                'original_price': 79.99,
                'discounted_price': 49.99,
                'discount_percentage': 38,
                'product_url': 'https://www.amazon.com/demo-product-2',
                'image_url': 'https://m.media-amazon.com/images/I/71z6z6z6z6L._AC_UL1500_.jpg',
                'source': 'amazon',
                'category': 'fashion',
                'deal_hash': 'test_hash_2'
            },
            {
                'title': 'Kitchen Knife Set - 15 Piece Professional',
                'original_price': 149.99,
                'discounted_price': 89.99,
                'discount_percentage': 40,
                'product_url': 'https://www.amazon.com/demo-product-3',
                'image_url': 'https://m.media-amazon.com/images/I/71j6z6z6z6L._AC_SL1500_.jpg',
                'source': 'amazon',
                'category': 'home',
                'deal_hash': 'test_hash_3'
            },
            {
                'title': 'Smart Watch with Fitness Tracker',
                'original_price': 199.99,
                'discounted_price': 129.99,
                'discount_percentage': 35,
                'product_url': 'https://www.amazon.com/demo-product-4',
                'image_url': 'https://m.media-amazon.com/images/I/71k6z6z6z6L._AC_SL1500_.jpg',
                'source': 'amazon',
                'category': 'electronics',
                'deal_hash': 'test_hash_4'
            },
            {
                'title': 'Yoga Mat - Non-Slip Exercise Mat',
                'original_price': 39.99,
                'discounted_price': 24.99,
                'discount_percentage': 38,
                'product_url': 'https://www.amazon.com/demo-product-5',
                'image_url': 'https://m.media-amazon.com/images/I/71l6z6z6z6L._AC_SL1500_.jpg',
                'source': 'amazon',
                'category': 'sports',
                'deal_hash': 'test_hash_5'
            }
        ]
        
        return test_deals