from django.shortcuts import render
from creator_listings.models import BlogListingCreationModel
from sponsor_listings.models import SponsorListingCreationModel

def creator_marketplace(request):
    creator_listings = BlogListingCreationModel.objects.all()

    context = {
        'creator_listings': creator_listings
    }

    return render(request, 'creator_marketplace.html', context)

def sponsor_marketplace(request):
    sponsor_listings = SponsorListingCreationModel.objects.all()

    context = {
        'sponsor_listings': sponsor_listings
    }

    return render(request, 'sponsor_marketplace.html', context)