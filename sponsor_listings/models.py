from django.db import models
from django.contrib.auth.models import User


class SponsorListingCreationModel(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)

    product = models.CharField(max_length=300, default=None, null=True, blank=True)
    niche = models.CharField(max_length=300, default=None, null=True, blank=True)
    money = models.CharField(max_length=300, default=None, null=True, blank=True)
    monthly_views_min = models.CharField(max_length=300, default=None, null=True, blank=True)
    sponsor_img = models.FileField(upload_to='uploads/', default=None, null=True, blank=True)

    tagline = models.CharField(max_length=120, default=None, null=True, blank=True)
    overview_description = models.CharField(max_length=50000, default=None, null=True, blank=True)
    audience_description = models.CharField(max_length=50000, default=None, null=True, blank=True)
    creator_description = models.CharField(max_length=50000, default=None, null=True, blank=True)

    url = models.CharField(max_length=1000, default=None, null=True, blank=True)

    def __str__(self):
        return self.product
