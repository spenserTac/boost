from sponsor_listings import views
from django.urls import path

urlpatterns = [
    path('', views.sponsor_listing_creation, name='sponsor_listing'),
    path('update/<int:id>/', views.sponsor_listing_update, name='sponsor_listing_update'),
    path('delete/<int:id>/', views.sponsor_listing_delete, name='sponsor_listing_delete'),
]