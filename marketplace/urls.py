from marketplace import views
from django.urls import path

urlpatterns = [
    path('creator_marketplace/', views.creator_marketplace, name='creator_marketplace'),
    path('creator_marketplace/<int:id>', views.creator_marketplace_listing_view, name='creator_marketplace_listing_view'),
    path('sponsor_marketplace/', views.sponsor_marketplace, name='sponsor_marketplace'),
    path('sponsor_marketplace/<int:id>', views.sponsor_marketplace_listing_view, name='sponsor_marketplace_listing_view'),
]