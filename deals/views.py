from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count
from .models import Deal, DealCategory, EcommerceSite

def home(request):
    # Get filter parameters
    category_slug = request.GET.get('category', '')
    sort = request.GET.get('sort', '-deal_score')
    
    # Build query
    deals_query = Deal.objects.filter(is_active=True)
    
    # Apply filters
    if category_slug:
        deals_query = deals_query.filter(category__slug=category_slug)
    
    # Apply sorting
    valid_sort_fields = ['-deal_score', '-discount_percentage', 'discounted_price']
    if sort in valid_sort_fields:
        deals_query = deals_query.order_by(sort)
    else:
        deals_query = deals_query.order_by('-deal_score')
    
    # Pagination
    paginator = Paginator(deals_query, 9)  # 9 deals per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Get categories
    categories = DealCategory.objects.all()
    
    # Get stats
    total_deals = Deal.objects.filter(is_active=True).count()
    sites_count = EcommerceSite.objects.filter(is_active=True).count()
    
    context = {
        'deals': page_obj,
        'categories': categories,
        'selected_category': category_slug,
        'total_deals': total_deals,
        'sites_count': sites_count,
    }
    
    return render(request, 'deals/home.html', context)

def today_deals(request):
    """Show today's best deals"""
    deals = Deal.objects.filter(is_active=True).order_by('-deal_score')[:9]
    
    context = {
        'deals': deals,
        'title': "Today's Best Deals"
    }
    
    return render(request, 'deals/home.html', context)

def about(request):
    """About page"""
    return render(request, 'deals/about.html')

def search_deals(request):
    """Simple search function"""
    query = request.GET.get('q', '').strip()
    
    if query:
        deals = Deal.objects.filter(
            is_active=True,
            title__icontains=query
        ).order_by('-deal_score')
    else:
        deals = Deal.objects.filter(is_active=True).order_by('-deal_score')
    
    paginator = Paginator(deals, 9)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'deals': page_obj,
        'query': query,
        'total_deals': deals.count()
    }
    
    return render(request, 'deals/home.html', context)