from django.shortcuts import render
from creator_listings.models import BlogListingCreationModel

def creator_marketplace(request):
    creator_listings = BlogListingCreationModel.objects.all()

    context = {
        'creator_listings': creator_listings
    }

    return render(request, 'creator_marketplace.html', context)