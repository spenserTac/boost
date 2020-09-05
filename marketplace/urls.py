from marketplace import views
from django.urls import path

urlpatterns = [
    path('creator_marketplace/', views.creator_marketplace, name='creator_marketplace'),
    path('creator_marketplace/<int:id>', views.creator_marketplace_listing_view, name='creator_marketplace_listing_view'),
    path('creator_marketplace/<int:id>/watch', views.creator_marketplace_listing_watch_view, name='creator_marketplace_listing_watch_view'),
    path('creator_marketplace/<int:id>/unwatch', views.creator_marketplace_listing_unwatch_view, name='creator_marketplace_listing_unwatch_view'),
    path('creator_marketplace/<int:id>/order', views.creator_marketplace_listing_order_view, name='creator_marketplace_listing_order_view'),
    path('creator_marketplace/<int:id>/unorder', views.creator_marketplace_listing_unorder_view, name='creator_marketplace_listing_unorder_view'),

    #path('creator_marketplace/<int:id>/order/detail', views.creator_marketplace_listing_order_detail_view, name='creator_marketplace_listing_order_detail_view'),

    
    path('sponsor_marketplace/', views.sponsor_marketplace, name='sponsor_marketplace'),
    path('sponsor_marketplace/<int:id>', views.sponsor_marketplace_listing_view, name='sponsor_marketplace_listing_view'),
    path('sponsor_marketplace/<int:id>/watch', views.sponsor_marketplace_listing_watch_view, name='sponsor_marketplace_listing_watch_view'),
    path('sponsor_marketplace/<int:id>/unwatch', views.sponsor_marketplace_listing_unwatch_view, name='sponsor_marketplace_listing_unwatch_view'),
    path('sponsor_marketplace/<int:id>/order', views.sponsor_marketplace_listing_order_view, name='sponsor_marketplace_listing_order_view'),
    path('sponsor_marketplace/<int:id>/unorder', views.sponsor_marketplace_listing_unorder_view, name='sponsor_marketplace_listing_unorder_view'),
    
    
]

