from django.db import models
from creator_listings.models import BlogListingCreationModel
from sponsor_listings.models import SponsorListingCreationModel
from django.contrib.auth.models import User

class UserWatchDashboardModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, blank=True, null=True)
    watched_creator = models.TextField(null=True)
    watched_sponsor = models.TextField(null=True)

