from django.db import models
from creator_listings.models import BlogListingCreationModel
from sponsor_listings.models import SponsorListingCreationModel
from django.contrib.auth.models import User

from django.utils import timezone




class SignUpMetricModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=True)

    date = models.DateField(default=timezone.now)

    def __str__(self):
        return (str(self.user) + ' - signup metric')









class CreatorListingMadeMetricModel(models.Model):
    listing_id = models.IntegerField(default=-1)

    ga_bool = models.CharField(max_length=50, blank=True, null=True)

    date = models.DateField(default=timezone.now)

    def __str__(self):
        return (str(self.listing_id) + ' - creator listing metric')




class SponsorListingMadeMetricModel(models.Model):
    listing_id = models.IntegerField(default=-1)

    date = models.DateField(default=timezone.now)

    def __str__(self):
        return (str(self.listing_id) + ' - sponsor listing metric')





class CreatorOrdersSponsorMetricModel(models.Model):
    order_id = models.IntegerField(default=-1)

    date = models.DateField(default=timezone.now)

    def __str__(self):
        return (str(self.order_id) + ' - creator orders sponsor metric')



class SponsorOrdersCreatorMetricModel(models.Model):
    order_id = models.IntegerField(default=-1)

    date = models.DateField(default=timezone.now)

    def __str__(self):
        return (str(self.order_id) + ' - sponsor orders creator metric')






class CreatorAccSponsorMetricModel(models.Model):
    order_id = models.IntegerField(default=-1)

    date = models.DateField(default=timezone.now)

    def __str__(self):
        return (str(self.order_id) + ' - creator acc sponsor metric')

class SponsorAccCreatorMetricModel(models.Model):
    order_id = models.IntegerField(default=-1)

    date = models.DateField(default=timezone.now)

    def __str__(self):
        return (str(self.order_id) + ' - sponsor acc creator metric')






class CreatorSendsContentMetricModel(models.Model):
    order_id = models.IntegerField(default=-1)

    date = models.DateField(default=timezone.now)

    def __str__(self):
        return (str(self.order_id) + ' - creator sends content metric')

class SponsorSendsEditsMetricModel(models.Model):
    order_id = models.IntegerField(default=-1)

    date = models.DateField(default=timezone.now)

    def __str__(self):
        return (str(self.order_id) + ' - sponsor sends edits metric')

class SponsorInitiatesEscrowMetricModel(models.Model):
    order_id = models.IntegerField(default=-1)

    date = models.DateField(default=timezone.now)

    def __str__(self):
        return (str(self.order_id) + ' - escrow initiated metric')

class CreatorSendsUrlMetricModel(models.Model):
    order_id = models.IntegerField(default=-1)

    date = models.DateField(default=timezone.now)

    def __str__(self):
        return (str(self.order_id) + ' - url sent metric')

class SponsorCantFindUrlMetricModel(models.Model):
    order_id = models.IntegerField(default=-1)

    date = models.DateField(default=timezone.now)

    def __str__(self):
        return (str(self.order_id) + ' - cant find url metric')

class CompleteOrderMetricModel(models.Model):
    order_id = models.IntegerField(default=-1)

    date = models.DateField(default=timezone.now)

    def __str__(self):
        return (str(self.order_id) + ' - complete order metric')




class CreatorWithdrawsMetricModel(models.Model):
    order_id = models.IntegerField(default=-1)

    date = models.DateField(default=timezone.now)

    def __str__(self):
        return (str(self.order_id) + ' - creator withdraw metric')
