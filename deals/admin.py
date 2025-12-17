from django.contrib import admin
from .models import *

@admin.register(EcommerceSite)
class EcommerceSiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'base_url', 'is_active']

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ['title', 'source_site', 'discounted_price', 'discount_percentage', 'is_active']
    list_filter = ['source_site', 'is_active']
    search_fields = ['title']

@admin.register(DealCategory)
class DealCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'slug']

@admin.register(DailyScrapeLog)
class DailyScrapeLogAdmin(admin.ModelAdmin):
    list_display = ['site', 'started_at', 'status', 'deals_found', 'deals_added']
    list_filter = ['status', 'site']