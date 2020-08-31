from users import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Watching and unwatching listings
    path('dashboard/unwatch_c/<int:id>/', views.dashboard_unwatch_c, name='dashboard_unwatch_c'),
    path('dashboard/unwatch_s/<int:id>/', views.dashboard_unwatch_s, name='dashboard_unwatch_s'),

    # Unordering listings
    path('dashboard/unorder_c/<int:id>/', views.dashboard_unorder_c, name='dashboard_unorder_c'),
    path('dashboard/unorder_s/<int:id>/', views.dashboard_unorder_s, name='dashboard_unorder_s'),

    # Accepting and declining orders
    path('dashboard/caccept/<int:id>/', views.dashboard_creator_order_accept, name='dashboard_creator_order_accept'),
    path('dashboard/cdecline/<int:id>/', views.dashboard_creator_order_decline, name='dashboard_creator_order_decline'),

    path('dashboard/saccept/<int:id>/', views.dashboard_sponsor_order_accept, name='dashboard_sponsor_order_accept'),
    path('dashboard/sdecline/<int:id>/', views.dashboard_sponsor_order_decline, name='dashboard_sponsor_order_decline'),

    path('dashboard/ccomplete/<int:id>/', views.dashboard_creator_order_complete, name='dashboard_creator_order_complete'),
    path('dashboard/scomplete/<int:id>/', views.dashboard_sponsor_order_complete, name='dashboard_sponsor_order_complete'),

    path('dashboard/withdraw/<int:id>/<int:a_id', views.dashboard_withdraw_order, name='dashboard_withdraw_order'),
]