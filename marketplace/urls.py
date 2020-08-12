from marketplace import views
from django.urls import path

urlpatterns = [
    path('', views.creator_marketplace, name='creator_marketplace'),
]