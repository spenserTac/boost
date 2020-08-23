import simplejson as json
from python_stuff.converter import string_to_list, list_to_string #self made python file

from django.shortcuts import render, redirect
from django.urls import reverse
from creator_listings.models import BlogListingCreationModel
from sponsor_listings.models import SponsorListingCreationModel
from users.models import Profile
from django.contrib.auth.models import User

#from .forms import UserWatchDashboardForm


#
# Creator Listing Stuff
#

# The creator marketplace page
def creator_marketplace(request):
    creator_listings = BlogListingCreationModel.objects.all()

    context = {
        'creator_listings': creator_listings
    }

    return render(request, 'creator_marketplace.html', context)

# The detail page of a creator marketplace listing
def creator_marketplace_listing_view(request, id=None):
    listing = BlogListingCreationModel.objects.get(id=id)
    user = User.objects.get(username=request.user.username) # current logged in user
    users_profile = Profile.objects.get(user=user) # current looged in user's Profile

    # Seeing if the currently loggin user is following this post
    if (listing in users_profile.creators_watched.all()):
        following = True
    else:
        following = False

    # Seeing if the currently loggin user has ordered this post
    if (listing in users_profile.creators_u_ordered.all()):
        ordered = True
    else:
        ordered = False
    
    context = {
        'listing': listing,
        'following': following,
        'ordered': ordered
    }

    return render(request, 'creator_marketplace_listing_view.html', context)


# The logic for watching and unwatching a listing
def creator_marketplace_listing_watch_view(request, id=None):
    listing = BlogListingCreationModel.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    profile.creators_watched.add(listing)
    return redirect(reverse('creator_marketplace_listing_view', kwargs={'id': listing.id}))

def creator_marketplace_listing_unwatch_view(request, id=None):
    listing = BlogListingCreationModel.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    profile.creators_watched.remove(listing)
    return redirect(reverse('creator_marketplace_listing_view', kwargs={'id': listing.id}))



# The logic for ordering and unordering a listing
def creator_marketplace_listing_order_view(request, id=None):
    listing = BlogListingCreationModel.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    profile.creators_u_ordered.add(listing)
    '''if (request.method == 'POST'):
        if form.is_valid():
            form.save(commit=False).creator = request.user
            form.save()

            return redirect(reverse('creator_marketplace_listing_view', kwargs={'id': listing.id}))'''
    return redirect(reverse('creator_marketplace_listing_view', kwargs={'id': listing.id}))

def creator_marketplace_listing_unorder_view(request, id=None):
    listing = BlogListingCreationModel.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    profile.creators_u_ordered.remove(listing)
    return redirect(reverse('creator_marketplace_listing_view', kwargs={'id': listing.id}))





#
# Sponsor Listing Stuff
#

# The sponsor marketplace page
def sponsor_marketplace(request):
    sponsor_listings = SponsorListingCreationModel.objects.all()

    context = {
        'sponsor_listings': sponsor_listings
    }

    return render(request, 'sponsor_marketplace.html', context)

# The detail page of a sponsor marketplace listing
def sponsor_marketplace_listing_view(request, id=None):
    listing = SponsorListingCreationModel.objects.get(id=id)
    user = User.objects.get(username=request.user.username) # current logged in user
    users_profile = Profile.objects.get(user=user) # current looged in user's Profile

    # Seeing if the currently loggin user is following this post
    if (listing in users_profile.sponsors_watched.all()):
        following = True
    else:
        following = False

    # Seeing if the currently loggin user has ordered this post
    if (listing in users_profile.sponsors_u_ordered.all()):
        ordered = True
    else:
        ordered = False

    context = {
        'listing': listing,
        'following': following,
        'ordered': ordered
    }

    return render(request, 'sponsor_marketplace_listing_view.html', context)



# The logic for watching and unwatching a listing
def sponsor_marketplace_listing_watch_view(request, id=None):
    listing = SponsorListingCreationModel.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    profile.sponsors_watched.add(listing)
    return redirect(reverse('sponsor_marketplace_listing_view', kwargs={'id': listing.id}))

def sponsor_marketplace_listing_unwatch_view(request, id=None):
    listing = SponsorListingCreationModel.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    profile.sponsors_watched.remove(listing)
    return redirect(reverse('sponsor_marketplace_listing_view', kwargs={'id': listing.id}))



# The logic for ordering and unordering a listing
def sponsor_marketplace_listing_order_view(request, id=None):
    listing = SponsorListingCreationModel.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    profile.sponsors_u_ordered.add(listing)
    return redirect(reverse('sponsor_marketplace_listing_view', kwargs={'id': listing.id}))

def sponsor_marketplace_listing_unorder_view(request, id=None):
    listing = SponsorListingCreationModel.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    profile.sponsors_u_ordered.remove(listing)
    return redirect(reverse('sponsor_marketplace_listing_view', kwargs={'id': listing.id}))