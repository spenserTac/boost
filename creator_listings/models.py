from django.db import models
from django.contrib.auth.models import User
import glob, os


class BlogListingCreationModel(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)

    ig_url = models.CharField(max_length=1000, default=None, null=True, blank=True) # this is the url to the page, since IG has a website.
    niche = models.CharField(max_length=300, default=None, null=True, blank=True)
    age = models.IntegerField(max_length=300, default=None, null=True, blank=True)

    monthly_views = models.IntegerField(default=None, null=True, blank=True) # useless

    tagline = models.CharField(max_length=10000, default=None, null=True, blank=True)
    overview_description = models.TextField(max_length=500000, default=None, null=True, blank=True)
    audience_description = models.TextField(max_length=500000, default=None, null=True, blank=True)
    sponsor_description = models.TextField(max_length=500000, default=None, null=True, blank=True)
    pricing_description = models.TextField(max_length=500000, default=None, null=True, blank=True)
    exp_description = models.TextField(max_length=500000, default=None, null=True, blank=True)

    email = models.CharField(max_length=300, default=None, null=True, blank=True)
    number = models.CharField(max_length=300, default=None, null=True, blank=True)

    language = models.CharField(max_length=300, default=None, null=True, blank=True)
    ig_type = models.CharField(max_length=300, default=None, null=True, blank=True)
    ig_name = models.CharField(max_length=300, default=None, null=True, blank=True) # this would be the handle.

    notification_type_email = models.CharField(max_length=30000, default=None, null=True, blank=True)
    notification_type_phone = models.CharField(max_length=30000, default=None, null=True, blank=True)
    search_keywords = models.CharField(max_length=30000, default=None, null=True, blank=True)


    followers = models.IntegerField(default=None, null=True, blank=True)
    avg_likes = models.IntegerField(default=None, null=True, blank=True)
    avg_comments = models.IntegerField(default=None, null=True, blank=True)
    engagement_rate = models.DecimalField(max_digits=4, decimal_places=2, default=None, null=True, blank=True)
    estimated_post_impressions = models.IntegerField(default=None, null=True, blank=True)

    # ================================================================================================================================================
    # followers - estimated_post_imppressions will all be added manually. Just go to phlanx.com, inzpire.com, influencermarketinghub.com, etc. to
    #             to add these data points in. Remember, this is a concirge MVP.
    # ================================================================================================================================================



    def google_a_csv_upload_path(instance, filename):
        # instance is the instance of the model.
        # if user creates a listing, the try will fail, if they're updating, the try will pass.
        try:
            if instance.google_a_csv:
                '''files = glob.glob('media/listings/creator/{0}/{1}/google_a'.format(instance.creator.id,instance.blog_name))
                print('---->   ', files)
                for f in files:
                    print('\nREMOVING: ', f)
                    os.remove(f)'''

                '''for f in os.listdir('media/listings/creator/{0}/{1}/google_a'.format(instance.creator.id,instance.blog_name)):
                    print('>>>>>>', f)
                    os.remove(os.path.join('media/listings/creator/{0}/{1}/google_a'.format(instance.creator.id,instance.blog_name)), f)'''

                return 'listings/creator/{0}/{1}/google_a/{2}'.format(instance.creator.id,instance.blog_name, filename)
        except:
            return 'listings/creator/{0}/{1}/google_a/{2}'.format(instance.creator.id,instance.blog_name, filename)

    #google_a_csv = models.FileField(upload_to=google_a_csv_upload_path, default=None, null=True, blank=True)

    def filename(self):
        return os.path.basename(self.google_a_csv.name)



    def listing_img_path(instance, filename):
        # instance is the instance of the model.
        # if user creates a listing, the try will fail, if they're updating, the try will pass.
        try:
            if instance.listing_img:
                '''files = glob.glob('media/listings/creator/{0}/{1}/listing_img'.format(instance.creator.id,instance.blog_name))
                for f in files:
                    os.remove(f)'''

                return 'listings/creator/{0}/{1}/listing_img/{2}'.format(instance.creator.id,instance.ig_name, filename)
        except:
            return 'listings/creator/{0}/{1}/listing_img/{2}'.format(instance.creator.id,instance.ig_name, filename)

    listing_img = models.ImageField(upload_to=listing_img_path, height_field=None, width_field=None, default=None, null=True, blank=True)

    def __str__(self):
        return self.ig_name or ""
