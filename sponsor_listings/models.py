from django.db import models
from django.contrib.auth.models import User


class SponsorListingCreationModel(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)

    product = models.CharField(max_length=300, default=None, null=True, blank=True)
    niche = models.CharField(max_length=300, default=None, null=True, blank=True)
    money = models.CharField(max_length=300, default=None, null=True, blank=True)
    monthly_views_min = models.CharField(max_length=300, default=None, null=True, blank=True)

    email = models.CharField(max_length=300, default=None, null=True, blank=True)
    number = models.CharField(max_length=300, default=None, null=True, blank=True)

    tagline = models.CharField(max_length=120, default=None, null=True, blank=True)
    overview_description = models.CharField(max_length=50000, default=None, null=True, blank=True)
    audience_description = models.CharField(max_length=50000, default=None, null=True, blank=True)
    creator_description = models.CharField(max_length=50000, default=None, null=True, blank=True)
    notification_type = models.CharField(max_length=30000, default=None, null=True, blank=True)

    url = models.CharField(max_length=1000, null=True, blank=True)

    def listing_img_path(instance, filename):
        # instance is the instance of the model.
        # if user creates a listing, the try will fail, if they're updating, the try will pass.
        try:
            if instance.listing_img:
                os.remove('media/listings/sponsor/{0}/{1}/listing_img/{2}'.format(instance.creator.id,instance.product, filename))
                return 'listings/sponsor/{0}/{1}/listing_img/{2}'.format(instance.creator.id,instance.product, filename)
        except:
            return 'listings/sponsor/{0}/{1}/listing_img/{2}'.format(instance.creator.id,instance.product, filename)
    listing_img = models.ImageField(upload_to=listing_img_path, height_field=None, width_field=None, default=None, null=True, blank=True)

    def __str__(self):
        return self.product
