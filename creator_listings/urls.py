from creator_listings import views
from django.urls import path

urlpatterns = [
    path('', views.blogger_listing_creation, name='blog_listing'),
]