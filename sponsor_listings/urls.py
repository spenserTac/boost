from sponsor_listings import views
from django.urls import path

urlpatterns = [
    path('', views.sponsor_listing_creation, name='sponsor_listing'),
]