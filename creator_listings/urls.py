from creator_listings import views
from django.urls import path

urlpatterns = [
    path('', views.blogger_listing_creation, name='blog_listing'),

    path('creator/', views.creator_listing_creation_type_c, name='creator_listing_creation_type_c'),

    path('update/<int:id>/', views.blogger_listing_update, name='blog_listing_update'),
    path('delete/<int:id>/', views.blogger_listing_delete, name='blog_listing_delete'),
]
