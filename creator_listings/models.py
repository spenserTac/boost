from django.db import models

class BlogListingCreationModel(models.Model):
    blog_url = models.CharField(max_length=300)
    niche = models.CharField(max_length=300)
    age = models.IntegerField()
    monthly_views = models.CharField(max_length=300)

    def __str__(self):
        return self.blog_url