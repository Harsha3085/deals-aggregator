from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('today/', views.today_deals, name='today_deals'),
    path('about/', views.about, name='about'),
    path('search/', views.search_deals, name='search_deals'),
]