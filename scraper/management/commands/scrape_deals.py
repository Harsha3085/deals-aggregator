from django.core.management.base import BaseCommand
from scraper.scraping_manager import ScrapingManager

class Command(BaseCommand):
    help = 'Run the daily deal scraping process'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--test',
            action='store_true',
            help='Run in test mode (uses demo data)'
        )
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting deal scraping...'))
        
        manager = ScrapingManager()
        test_mode = options.get('test', True)
        
        results = manager.run_scraping(test_mode=test_mode)
        
        # Print results
        for site, stats in results.items():
            self.stdout.write(
                self.style.SUCCESS(
                    f"{site}: Found {stats['found']} deals, "
                    f"Added {stats['added']} new deals"
                )
            )
        
        self.stdout.write(self.style.SUCCESS('Scraping completed!'))