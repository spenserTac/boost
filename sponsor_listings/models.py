from django.db import models
from django.contrib.auth.models import User

class SponsorListingCreationModel(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    product = models.CharField(max_length=300)
    niche = models.CharField(max_length=300)
    money = models.CharField(max_length=300)
    monthly_views_min = models.CharField(max_length=300)

    def __str__(self):
        return self.product