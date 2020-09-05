import django_filters

from creator_listings.models import BlogListingCreationModel
from sponsor_listings.models import SponsorListingCreationModel

class CreatorListingFilter(django_filters.FilterSet):
    class Meta:
        model = BlogListingCreationModel
        fields = ['niche', 'age', 'monthly_views']

class SponsorListingFilter(django_filters.FilterSet):
    class Meta:
        model = SponsorListingCreationModel
        fields = ['niche', 'money', 'monthly_views_min']