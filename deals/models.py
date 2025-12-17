from django.db import models
from django.utils import timezone
import hashlib

class EcommerceSite(models.Model):
    name = models.CharField(max_length=100)
    base_url = models.URLField()
    deals_page_url = models.URLField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class DealCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Deal(models.Model):
    # Basic Info
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    
    # Pricing
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.IntegerField()
    currency = models.CharField(max_length=3, default='USD')
    
    # Product Info
    product_url = models.URLField()
    image_url = models.URLField(blank=True)
    brand = models.CharField(max_length=100, blank=True)
    
    # Categorization
    category = models.ForeignKey(DealCategory, on_delete=models.SET_NULL, null=True)
    tags = models.CharField(max_length=500, blank=True)
    
    # Source Info
    source_site = models.ForeignKey(EcommerceSite, on_delete=models.CASCADE)
    
    # Tracking
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    valid_until = models.DateTimeField(null=True, blank=True)
    last_checked = models.DateTimeField(auto_now=True)
    first_seen = models.DateTimeField(auto_now_add=True)
    
    # Engagement Metrics
    click_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    
    # Quality Metrics
    deal_score = models.IntegerField(default=0)
    
    # Hash for deduplication
    deal_hash = models.CharField(max_length=64, unique=True)
    
    def save(self, *args, **kwargs):
        # Generate unique hash before saving
        if not self.deal_hash:
            hash_string = f"{self.title}_{self.source_site.name}_{self.discounted_price}"
            self.deal_hash = hashlib.sha256(hash_string.encode()).hexdigest()
        
        # Auto-calculate discount percentage if not provided
        if self.original_price and self.discounted_price and not self.discount_percentage:
            discount = ((self.original_price - self.discounted_price) / self.original_price) * 100
            self.discount_percentage = int(discount)
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title[:50]}... ({self.source_site.name})"

class DailyScrapeLog(models.Model):
    site = models.ForeignKey(EcommerceSite, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    deals_found = models.IntegerField(default=0)
    deals_added = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='pending')
    error_message = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.site.name} - {self.started_at.date()}"

class UserClick(models.Model):
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    clicked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['clicked_at', 'deal']),
        ]