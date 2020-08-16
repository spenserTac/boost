from django.db import models
from django.contrib.auth.models import User

class BlogListingCreationModel(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    blog_url = models.CharField(max_length=300)
    niche = models.CharField(max_length=300)
    age = models.CharField(max_length=300)
    monthly_views = models.CharField(max_length=300)

    def __str__(self):
        return self.blog_url