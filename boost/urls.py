"""boost URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from essentials import views as essentials_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', essentials_views.home, name='home'),
    path('cookies-policy', essentials_views.cookies_policy, name='cookies_policy'),
    path('disclaimer-policy', essentials_views.disclaimer_policy, name='disclaimer_policy'),
    path('terms-and-conditions', essentials_views.terms_and_conditions, name='terms_and_conditions'),
    path('return-policy', essentials_views.return_policy, name='return_policy'),
    path('privacy-policy', essentials_views.privacy_policy, name='privacy_policy'),
    path('about-us', essentials_views.about_us, name='about_us'),




    path('creators/', include('creator_listings.urls')),
    path('sponsors/', include('sponsor_listings.urls')),
    path('marketplace/', include('marketplace.urls')),
    path('account/', include('users.urls')),

    # Google login
    path('accounts/', include('allauth.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
