from django.contrib import admin
from .models import *


admin.site.register(SignUpMetricModel)


admin.site.register(CreatorListingMadeMetricModel)
admin.site.register(SponsorListingMadeMetricModel)
admin.site.register(CreatorOrdersSponsorMetricModel)
admin.site.register(SponsorOrdersCreatorMetricModel)
admin.site.register(CreatorAccSponsorMetricModel)
admin.site.register(SponsorAccCreatorMetricModel)
admin.site.register(CreatorSendsContentMetricModel)
admin.site.register(SponsorSendsEditsMetricModel)
admin.site.register(SponsorInitiatesEscrowMetricModel)
admin.site.register(CreatorSendsUrlMetricModel)
admin.site.register(SponsorCantFindUrlMetricModel)
admin.site.register(CompleteOrderMetricModel)
admin.site.register(CreatorWithdrawsMetricModel)
