from django.db import models
from creator_listings.models import BlogListingCreationModel
from sponsor_listings.models import SponsorListingCreationModel
from django.contrib.auth.models import User


'''

!!! Add ability to add pictures, files, and urls to orders. And any other stuff that may be necessary.

'''


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=True)

    creators_watched = models.ManyToManyField(BlogListingCreationModel, blank=True, related_name='creators_watching')
    sponsors_watched = models.ManyToManyField(SponsorListingCreationModel, blank=True, related_name='sponsors_watching')

    creators_u_ordered = models.ManyToManyField(BlogListingCreationModel, blank=True, related_name='creators_u_ordered')
    sponsors_u_ordered = models.ManyToManyField(SponsorListingCreationModel, blank=True, related_name='sponsors_u_ordered')

    creators_who_ordered_u = models.ManyToManyField(BlogListingCreationModel, blank=True, related_name='creators_who_ordered_u')
    sponsors_who_ordered_u = models.ManyToManyField(SponsorListingCreationModel, blank=True, related_name='sponsors_who_ordered_u')

    type = models.CharField(max_length=320, default='none', null=True, blank=True)

    def __str__(self):
        return (str(self.user) + '\'s profile')

    def profiles_listings(self):
        return self.bloglistingcreationmodel_set.all(), self.sponsorlistingcreationset.all()




# Models for users orders (creators orders and sponsor orders)

# Orders for creators (creators will see these in their dashboard where they can review, accept/deny them. The "buyer" will then be notified
#       via email and text)
class CreatorOrderModel(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='buyer_username_creator_order')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='creator_username_creator_listing')
    creator_listing = models.ForeignKey(BlogListingCreationModel, blank=True, on_delete=models.CASCADE, null=True, related_name='creator_listing')


    buyer_listing = models.CharField(max_length=500, blank=True, null=True)


    buyers_listing_s = models.ForeignKey(SponsorListingCreationModel, on_delete=models.CASCADE, blank=True, null=True, related_name="buyers_s_listing_for_c_order")
    buyers_listing_c = models.ForeignKey(BlogListingCreationModel, on_delete=models.CASCADE, blank=True, null=True, related_name="buyers_c_listing_for_c_order")

    service = models.CharField(max_length=500, blank=True, null=True)
    service_detailed = models.TextField(max_length=1000, blank=True, null=True)

    # Accepted, denied, or the default in review
    status = models.CharField(max_length=100, blank=True, null=True, default='In Review')

    payout = models.CharField(max_length=10000, blank=True, null=True, default=0)


    def s_content_file_path(instance, filename):
        # instance is the instance of the model.
        # if user creates a listing, the try will fail, if they're updating, the try will pass.
        try:
            if instance.s_content_file:
                os.remove('media/orders/initial_orders/%s/s_content_file/%s' % (str(instance.buyer.id)+'--'+str(instance.creator.id), filename))
                return 'orders/initial_orders/%s/s_content_file/%s' % (str(instance.buyer.id)+'--'+str(instance.creator.id), filename)
        except:
            return 'orders/initial_orders/%s/s_content_file/%s' % (str(instance.buyer.id)+'--'+str(instance.creator.id), filename)

    s_content_file = models.FileField(upload_to=s_content_file_path, default=None, null=True, blank=True)



    def __str__(self):
        return ('BUYER: ' + str(self.buyer) + ' | CREATOR: ' + str(self.creator_listing))


# Orders for sponsors (sponsors will see these in their dashboard where they can review, accept/deny them. The "buyer" (only creators)
#       will then be notified via email and text)
class SponsorOrderModel(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='buyer_username_sponsor_order')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='creator_username_sponsor_listing')
    sponsor_listing = models.ForeignKey(SponsorListingCreationModel, blank=True, on_delete=models.CASCADE, related_name='sponsor_listing')

    buyer_listing = models.CharField(max_length=500, blank=True, null=True)

    buyers_listing_s = models.ForeignKey(SponsorListingCreationModel, on_delete=models.CASCADE, blank=True, null=True, related_name="buyers_s_listing_for_s_order")
    buyers_listing_c = models.ForeignKey(BlogListingCreationModel, on_delete=models.CASCADE, blank=True, null=True, related_name="buyers_c_listing_for_s_order")

    services_creator_is_willing_to_provide = models.CharField(max_length=500, blank=False)
    services_creator_is_willing_to_provide_detailed = models.TextField(max_length=1000, blank=True)

    # Accepted, denied, or the default in review
    status = models.CharField(max_length=100, blank=True, null=True, default='In Review')

    def __str__(self):
        return ('BUYER: ' + str(self.buyer) + ' | CREATOR: ' + str(self.sponsor_listing))


class AcceptedCreatorOrderModel(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='buyer_username_accepted_creator_order')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='creator_username_accepted_creator_listing')
    creator_listing = models.ForeignKey(BlogListingCreationModel, blank=True, on_delete=models.CASCADE, null=True, related_name='accepted_creator_listing')


    buyer_listing = models.CharField(max_length=500, blank=True, null=True)


    buyers_listing_s = models.ForeignKey(SponsorListingCreationModel, on_delete=models.CASCADE, blank=True, null=True, related_name="buyers_accepted_s_listing_for_c_order")
    buyers_listing_c = models.ForeignKey(BlogListingCreationModel, on_delete=models.CASCADE, blank=True, null=True, related_name="buyers_accepted_c_listing_for_c_order")

    service = models.CharField(max_length=500, blank=True, null=True)
    service_detailed = models.TextField(max_length=1000, blank=True, null=True)

    # Accepted, denied, or the default in review
    status = models.CharField(max_length=100, blank=True, null=True)
    who_initiated_order = models.CharField(max_length=100, blank=True, null=True)
    sponsor_approves = models.BooleanField(default=False, null=False)
    turn = models.CharField(default='c', max_length=10, blank=True, null=True)
    edits = models.CharField(max_length=10000, blank=True, null=True)
    payout = models.CharField(max_length=10000,default=0, blank=True, null=True)

    token = models.BinaryField(max_length=1000, blank=True, null=True, editable=True)
    transaction_id = models.BinaryField(max_length=1000, blank=True, null=True, editable=True)

    escrow_stage =  models.CharField(max_length=1000, blank=True, null=True)

    def review_file_path(instance, filename):
        # instance is the instance of the model.
        # if user creates a listing, the try will fail, if they're updating, the try will pass.
        try:
            if instance.review_file:
                os.remove('media/orders/escrow_orders/%s/review_file/%s' % (str(instance.buyer.id)+'--'+str(instance.creator.id), filename))
                return 'orders/escrow_orders/%s/review_file/%s' % (str(instance.buyer.id)+'--'+str(instance.creator.id), filename)
        except:
            return 'orders/escrow_orders/%s/review_file/%s' % (str(instance.buyer.id)+'--'+str(instance.creator.id), filename)
    review_file = models.FileField(upload_to=review_file_path, default=None, null=True, blank=True)


    def s_content_file_path(instance, filename):
        # instance is the instance of the model.
        # if user creates a listing, the try will fail, if they're updating, the try will pass.
        try:
            if instance.s_content_file:
                os.remove('media/orders/acc_orders/%s/s_content_file/%s' % (str(instance.buyer.id)+'--'+str(instance.creator.id), filename))
                return 'orders/acc_orders/%s/s_content_file/%s' % (str(instance.buyer.id)+'--'+str(instance.creator.id), filename)
        except:
            return 'orders/acc_orders/%s/s_content_file/%s' % (str(instance.buyer.id)+'--'+str(instance.creator.id), filename)

    s_content_file = models.FileField(upload_to=s_content_file_path, default=None, null=True, blank=True)

    def __str__(self):
        return ('STATUS: ' + str(self.status) + ' | BUYER: ' + str(self.buyer) + ' | CREATOR: ' + str(self.creator_listing))



class AcceptedSponsorOrderModel(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='buyer_username_accepted_sponsor_order')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='creator_username_accepted_sponsor_listing')
    sponsor_listing = models.ForeignKey(SponsorListingCreationModel, blank=True, on_delete=models.CASCADE, related_name='accepted_sponsor_listing')

    buyer_listing = models.CharField(max_length=500, blank=True, null=True)

    buyers_listing_s = models.ForeignKey(SponsorListingCreationModel, on_delete=models.CASCADE, blank=True, null=True, related_name="buyers_accepted_s_listing_for_s_order")
    buyers_listing_c = models.ForeignKey(BlogListingCreationModel, on_delete=models.CASCADE, blank=True, null=True, related_name="buyers_accepted_c_listing_for_s_order")

    services_creator_is_willing_to_provide = models.CharField(max_length=500, blank=False)
    services_creator_is_willing_to_provide_detailed = models.TextField(max_length=1000, blank=True)

    # Accepted, denied, or the default in review
    status = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return ('BUYER: ' + str(self.buyer) + ' | CREATOR: ' + str(self.sponsor_listing))


class CompletedOrderModel(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='buyer_username_completed_creator_order')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='creator_username_completed_creator_listing')
    creator_listing = models.ForeignKey(BlogListingCreationModel, blank=True, on_delete=models.CASCADE, null=True, related_name='completed_creator_listing')


    buyer_listing = models.CharField(max_length=500, blank=True, null=True)


    buyers_listing_s = models.ForeignKey(SponsorListingCreationModel, on_delete=models.CASCADE, blank=True, null=True, related_name="buyers_completed_s_listing_for_c_order")
    buyers_listing_c = models.ForeignKey(BlogListingCreationModel, on_delete=models.CASCADE, blank=True, null=True, related_name="buyers_completed_c_listing_for_c_order")

    service = models.CharField(max_length=500, blank=True, null=True)
    service_detailed = models.TextField(max_length=1000, blank=True, null=True)

    # Accepted, denied, or the default in review
    status = models.CharField(max_length=100, blank=True, null=True)

    who_initiated_order = models.CharField(max_length=100, blank=True, null=True)

    payout = models.CharField(max_length=100000, blank=True, null=True)

    def __str__(self):
        return ('BUYER: ' + str(self.buyer) + ' | CREATOR: ' + str(self.creator_listing))


class SupportTicket(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='support_ticket_creator')
    email = models.CharField(max_length=500, blank=True, null=True)
    problem = models.TextField(max_length=5000, blank=True, null=True)

    def __str__(self):
        return('CREATOR: ' + str(self.creator) + 'EMAIL: ' + str(self.email))


class FeatureTicket(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='feature_request_creator')
    email = models.CharField(max_length=500, blank=True, null=True)
    feature = models.TextField(max_length=5000, blank=True, null=True)

    def __str__(self):
        return('CREATOR: ' + str(self.creator) + ' - EMAIL: ' + str(self.email))
