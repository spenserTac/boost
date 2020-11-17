from django.db import models
from django.contrib.auth.models import User


class BlogListingCreationModel(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    blog_url = models.CharField(max_length=1000, default=None, null=True, blank=True)
    niche = models.CharField(max_length=300, default=None, null=True, blank=True)
    age = models.IntegerField(max_length=300, default=None, null=True, blank=True)
    monthly_views = models.CharField(max_length=300, default=None, null=True, blank=True)

    tagline = models.CharField(max_length=1000, default=None, null=True, blank=True)
    overview_description = models.TextField(max_length=500000, default=None, null=True, blank=True)
    audience_description = models.TextField(max_length=500000, default=None, null=True, blank=True)
    sponsor_description = models.TextField(max_length=500000, default=None, null=True, blank=True)

    email = models.CharField(max_length=300, default=None, null=True, blank=True)
    number = models.CharField(max_length=300, default=None, null=True, blank=True)
    language = models.CharField(max_length=300, default=None, null=True, blank=True)
    blog_type = models.CharField(max_length=300, default=None, null=True, blank=True)
    blog_name = models.CharField(max_length=300, default=None, null=True, blank=True)
    notification_type = models.CharField(max_length=30000, default=None, null=True, blank=True)
    search_keywords = models.CharField(max_length=30000, default=None, null=True, blank=True)



    def google_a_csv_upload_path(instance, filename):
        # instance is the instance of the model.
        # if user creates a listing, the try will fail, if they're updating, the try will pass.
        try:
            if instance.google_a_csv:
                os.remove('media/listings/creator/{0}/{1}/google_a/{2}'.format(instance.creator.id,instance.blog_name, filename))
                return 'listings/creator/{0}/{1}/google_a/{2}'.format(instance.creator.id,instance.blog_name, filename)
        except:
            return 'listings/creator/{0}/{1}/google_a/{2}'.format(instance.creator.id,instance.blog_name, filename)
    google_a_csv = models.FileField(upload_to=google_a_csv_upload_path, default=None, null=True, blank=True)

    def listing_img_path(instance, filename):
        # instance is the instance of the model.
        # if user creates a listing, the try will fail, if they're updating, the try will pass.
        try:
            if instance.listing_img:
                os.remove('media/listings/creator/{0}/{1}/listing_img/{2}'.format(instance.creator.id,instance.blog_name, filename))
                return 'listings/creator/{0}/{1}/listing_img/{2}'.format(instance.creator.id,instance.blog_name, filename)
        except:
            return 'listings/creator/{0}/{1}/listing_img/{2}'.format(instance.creator.id,instance.blog_name, filename)
    listing_img = models.ImageField(upload_to=listing_img_path, height_field=None, width_field=None, default=None, null=True, blank=True)

    def __str__(self):
        return self.blog_name or ""
