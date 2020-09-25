from django.db import models
from django.contrib.auth.models import User


class BlogListingCreationModel(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    blog_url = models.CharField(max_length=1000, default=None, null=True, blank=True)
    niche = models.CharField(max_length=300, default=None, null=True, blank=True)
    age = models.CharField(max_length=300, default=None, null=True, blank=True)
    monthly_views = models.CharField(max_length=300, default=None, null=True, blank=True)

    tagline = models.CharField(max_length=120, default=None, null=True, blank=True)
    overview_description = models.CharField(max_length=50000, default=None, null=True, blank=True)
    audience_description = models.CharField(max_length=50000, default=None, null=True, blank=True)
    sponsor_description = models.CharField(max_length=50000, default=None, null=True, blank=True)
    
    email = models.CharField(max_length=300, default=None, null=True, blank=True)
    number = models.CharField(max_length=300, default=None, null=True, blank=True)
    language = models.CharField(max_length=300, default=None, null=True, blank=True)
    blog_type = models.CharField(max_length=300, default=None, null=True, blank=True)
    blog_name = models.CharField(max_length=300, default=None, null=True, blank=True)
    google_a_csv = models.FileField(upload_to='uploads/', default=None, null=True, blank=True)
    paypal_email = models.CharField(max_length=300, default=None, null=True, blank=True)
    creator_img = models.ImageField(upload_to='uploads/', default=None, null=True, blank=True)

    def __str__(self):
        return self.blog_url or ""