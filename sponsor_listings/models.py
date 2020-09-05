from django.db import models
from django.contrib.auth.models import User


class SponsorListingCreationModel(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    product = models.CharField(max_length=300, default=None)
    niche = models.CharField(max_length=300, default=None)
    money = models.CharField(max_length=300, default=None)
    monthly_views_min = models.CharField(max_length=300, default=None)
    #look_site_age = models.CharField(max_length=300, default=None)
    #look_language = models.CharField(max_length=300, default=None)
    #look_blog_type = models.CharField(max_length=300, default=None)

    def __str__(self):
        return self.product