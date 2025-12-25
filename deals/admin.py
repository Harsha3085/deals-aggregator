from django.contrib import admin
from .models import EcommerceSite, DealCategory, Deal, DailyScrapeLog, UserClick

# Simple admin for EcommerceSite
@admin.register(EcommerceSite)
class EcommerceSiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_url', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'base_url')

# FIXED: DealAdmin with working list_display
@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    # Use a custom method for title to avoid the error
    list_display = ('get_short_title', 'source_site', 'discounted_price', 
                    'discount_percentage', 'is_active', 'click_count')
    list_filter = ('source_site', 'is_active', 'category')
    search_fields = ('title', 'description', 'brand')
    readonly_fields = ('deal_hash', 'click_count', 'view_count', 
                       'first_seen', 'last_checked')
    
    # Custom method to display title
    def get_short_title(self, obj):
        return obj.title[:50] + "..." if len(obj.title) > 50 else obj.title
    get_short_title.short_description = 'Title'
    get_short_title.admin_order_field = 'title'
    
    # Admin actions
    def activate_deals(self, request, queryset):
        queryset.update(is_active=True)
    activate_deals.short_description = "Activate selected deals"
    
    def deactivate_deals(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_deals.short_description = "Deactivate selected deals"

# Simple admin for DealCategory
@admin.register(DealCategory)
class DealCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

# Simple admin for DailyScrapeLog
@admin.register(DailyScrapeLog)
class DailyScrapeLogAdmin(admin.ModelAdmin):
    list_display = ('site', 'started_at', 'status', 'deals_found', 'deals_added')
    list_filter = ('status', 'site')
    readonly_fields = ('started_at', 'finished_at')

# Simple admin for UserClick
@admin.register(UserClick)
class UserClickAdmin(admin.ModelAdmin):
    list_display = ('deal', 'ip_address', 'clicked_at')
    list_filter = ('clicked_at', 'deal')
    search_fields = ('ip_address', 'deal__title')