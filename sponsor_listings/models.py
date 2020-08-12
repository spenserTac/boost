from django.db import models

class SponsorListingCreationModel(models.Model):
    product = models.CharField(max_length=300)
    niche = models.CharField(max_length=300)
    money = models.IntegerField()
    monthly_views_min = models.CharField(max_length=300)

    def __str__(self):
        return self.product