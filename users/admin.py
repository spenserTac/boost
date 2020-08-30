from django.contrib import admin
from .models import Profile, CreatorOrderModel, SponsorOrderModel, AcceptedCreatorOrderModel, AcceptedSponsorOrderModel

admin.site.register(Profile)
admin.site.register(CreatorOrderModel)
admin.site.register(SponsorOrderModel)
admin.site.register(AcceptedCreatorOrderModel)
admin.site.register(AcceptedSponsorOrderModel)
