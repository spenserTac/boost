from django.contrib import admin
from .models import Profile, CreatorOrderModel, SponsorOrderModel

admin.site.register(Profile)
admin.site.register(CreatorOrderModel)
admin.site.register(SponsorOrderModel)