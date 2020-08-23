from django.db import models
from creator_listings.models import BlogListingCreationModel
from sponsor_listings.models import SponsorListingCreationModel
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=True)

    creators_watched = models.ManyToManyField(BlogListingCreationModel, blank=True, related_name='creators_watching')
    sponsors_watched = models.ManyToManyField(SponsorListingCreationModel, blank=True, related_name='sponsors_watching')

    creators_u_ordered = models.ManyToManyField(BlogListingCreationModel, blank=True, related_name='creators_u_ordered')
    sponsors_u_ordered = models.ManyToManyField(SponsorListingCreationModel, blank=True, related_name='sponsors_u_ordered')

    creators_who_ordered_u = models.ManyToManyField(BlogListingCreationModel, blank=True, related_name='creators_who_ordered_u')
    sponsors_who_ordered_u = models.ManyToManyField(SponsorListingCreationModel, blank=True, related_name='sponsors_who_ordered_u')


    '''def __str__(self):
        return (str(self.user) + '\'s profile')'''

    def profiles_listings(self):
        return self.bloglistingcreationmodel_set.all(), self.sponsorlistingcreationset.all()




# Models for users orders (creators orders and sponsor orders)

# Orders for creators (creators will see these in their dashboard where they can review, accept/deny them. The "buyer" will then be notified
#       via email and text)
class CreatorOrderModel(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    creator_listing = models.ForeignKey(BlogListingCreationModel, on_delete=models.CASCADE, related_name='creator_listing')

    # If it's a sponsor ordering a creator
    buyers_listing_for_sponsor = models.ForeignKey(SponsorListingCreationModel, on_delete=models.CASCADE, blank=True, null=True)
    what_services_sponsor_is_looking_for = models.CharField(max_length=500, blank=True, null=True)
    what_services_sponsor_is_looking_for_detailed = models.TextField(max_length=1000, blank=True, null=True)


    # If it's a creator ordering a creator (probably for a shoutout)
    buyers_listing_for_creator = models.ForeignKey(BlogListingCreationModel, on_delete=models.CASCADE,blank=True, null=True, related_name='buyers_creator_listing')
    what_services_creator_is_looking_for = models.CharField(max_length=500, blank=True, null=True)
    what_services_creator_is_looking_fordetailed = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return ('BUYER: [SPONSOR] ' + str(self.buyers_listing_for_sponsor) + ' - [CREATOR] ' + str(self.buyers_listing_for_creator) + ' | CREATOR: ' + str(self.creator_listing))


# Orders for sponsors (sponsors will see these in their dashboard where they can review, accept/deny them. The "buyer" (only creators)
#       will then be notified via email and text)
class SponsorOrderModel(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    sponsor_listing = models.ForeignKey(SponsorListingCreationModel, on_delete=models.CASCADE)

    # This is the buyer, who technically isn't buying anything, they're basically asking the sponsor if they'd like to
    #       sponsor them
    buyers_listing_for_creator = models.ForeignKey(BlogListingCreationModel, on_delete=models.CASCADE)
    services_creator_is_willing_to_provide = models.CharField(max_length=500, blank=False)
    services_creator_is_willing_to_provide_detailed = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return ('BUYER: [CREATOR]' + str(self.buyer) + ' | SPONSOR: ' + str(self.sponsor_listing))







