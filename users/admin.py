from django.contrib import admin
from .models import (Profile, CreatorOrderModel, SponsorOrderModel, AcceptedCreatorOrderModel, AcceptedSponsorOrderModel,
CompletedOrderModel, SupportTicket, SupportTicket, FeatureTicket)

admin.site.register(Profile)
admin.site.register(CreatorOrderModel)
admin.site.register(SponsorOrderModel)
admin.site.register(AcceptedCreatorOrderModel)
admin.site.register(AcceptedSponsorOrderModel)
admin.site.register(CompletedOrderModel)
admin.site.register(SupportTicket)
admin.site.register(FeatureTicket)
