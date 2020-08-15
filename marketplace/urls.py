from marketplace import views
from django.urls import path

urlpatterns = [
    path('creator_marketplace/', views.creator_marketplace, name='creator_marketplace'),
    path('sponsor_marketplace/', views.sponsor_marketplace, name='sponsor_marketplace'),
]