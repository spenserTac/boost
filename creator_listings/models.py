from django.db import models
from django.contrib.auth.models import User


class BlogListingCreationModel(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    blog_url = models.CharField(max_length=1000, default=None)
    niche = models.CharField(max_length=300, default=None)
    age = models.CharField(max_length=300, default=None)
    monthly_views = models.CharField(max_length=300, default=None)
    #description = models.CharField(max_length=30000, default=None)
    #language = models.CharField(max_length=300, default=None)
    #blog_catagory = models.CharField(max_length=300, default=None)
    #blog_name = models.CharField(max_length=300, default=None)

    def __str__(self):
        return self.blog_url