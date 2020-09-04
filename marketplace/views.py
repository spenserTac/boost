import simplejson as json
# self made python file

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from creator_listings.models import BlogListingCreationModel
from sponsor_listings.models import SponsorListingCreationModel
from users.models import Profile, CreatorOrderModel, SponsorOrderModel
from users.forms import CreatorOrderForm, SponsorOrderForm


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

@login_required(login_url='login')
def creator_marketplace_listing_view(request, id=None):
    listing = BlogListingCreationModel.objects.get(id=id)
    # current logged in user
    user = User.objects.get(username=request.user.username)
    # current looged in user's Profile
    users_profile = Profile.objects.get(user=user)

    # Seeing if the currently loggin user is following this post
    if (listing in users_profile.creators_watched.all()):
        following = True
    else:
        following = False


    creator_listing_exists = None
    try:
        l = CreatorOrderModel.objects.get(buyer=user, creator_listing=listing)
        creator_listing_exists = True
    except CreatorOrderModel.DoesNotExist:
        pass     

    # Seeing if the currently loggin user has ordered this post
    if (listing in users_profile.creators_u_ordered.all() and creator_listing_exists):
        ordered = True
    else:
        ordered = False

    context = {
        'listing': listing,
        'following': following,
        'ordered': ordered
    }

    return render(request, 'creator_marketplace_listing_view.html', context)

##### watching #####

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

##### ordering #####

# The logic for ordering and unordering a listing


def creator_marketplace_listing_order_view(request, id=None):
    listing = BlogListingCreationModel.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    profile.creators_u_ordered.add(listing)

    buyer = request.user
    buyer_profile = Profile.objects.get(user=buyer)
    buyers_sponsor_listings = buyer.sponsorlistingcreationmodel_set.all()
    buyers_creator_listings = buyer.bloglistingcreationmodel_set.all()

    creator = listing.creator

    prev_c_order = None

    try:
        prev_c_order = CreatorOrderModel.objects.get(buyer=buyer, creator_listing=listing)
    except:
        prev_c_order = None

    

    if (request.method == 'POST'):
        # add instance field for updating -> , instance=prev_c_order
        form = CreatorOrderForm(request.POST, instance=prev_c_order)

        if (form.is_valid()):
            obj = form.save(commit=False)

            obj.buyer = buyer
            obj.creator = creator
            obj.creator_listing = listing

            buyer_listing = form.cleaned_data['buyer_listing']
            creator_l = BlogListingCreationModel.objects.all()
            sponsor_l = SponsorListingCreationModel.objects.all()

            for l in creator_l:
                if (str(l) == str(buyer_listing)):
                    obj.buyers_listing_c = l

            for l in sponsor_l:
                if (str(l) == str(buyer_listing)):
                    obj.buyers_listing_s = l

            obj.save()

        return redirect(reverse('creator_marketplace_listing_view', kwargs={'id': listing.id}))

    context = {
        'buyer': buyer,
        'creator': creator,
        'buyers_sponsor_listings': buyers_sponsor_listings,
        'buyers_creator_listings': buyers_creator_listings,
        'prev_c_order': prev_c_order
    }

    return render(request, 'creator_marketplace_listing_order_detail_view.html', context)
    # return redirect(reverse('creator_marketplace_listing_view', kwargs={'id': listing.id}))


def creator_marketplace_listing_unorder_view(request, id=None):
    marketplace_c_listing = BlogListingCreationModel.objects.get(id=id)
    current_users_profile = Profile.objects.get(user=request.user)
    creator_order = CreatorOrderModel.objects.get(buyer=request.user, creator_listing=marketplace_c_listing)

    creator_order.delete()
    current_users_profile.creators_u_ordered.remove(marketplace_c_listing)
    return redirect(reverse('creator_marketplace_listing_view', kwargs={'id': marketplace_c_listing.id}))


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

@login_required(login_url='login')
def sponsor_marketplace_listing_view(request, id=None):
    listing = SponsorListingCreationModel.objects.get(id=id)
    # current logged in user
    user = User.objects.get(username=request.user.username)
    # current looged in user's Profile
    users_profile = Profile.objects.get(user=user)

    # Seeing if the currently loggin user is following this post
    if (listing in users_profile.sponsors_watched.all()):
        following = True
    else:
        following = False

    sponsor_listing_exists = None
    try:
        l = SponsorOrderModel.objects.get(buyer=user, sponsor_listing=listing)
        sponsor_listing_exists = True
    except SponsorOrderModel.DoesNotExist:
        pass

    # Seeing if the currently loggin user has ordered this post
    if (listing in users_profile.sponsors_u_ordered.all() and sponsor_listing_exists):
        ordered = True
    else:
        ordered = False

    context = {
        'listing': listing,
        'following': following,
        'ordered': ordered
    }

    return render(request, 'sponsor_marketplace_listing_view.html', context)

##### watching #####

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

##### ordering #####

# The logic for ordering and unordering a listing


def sponsor_marketplace_listing_order_view(request, id=None):
    listing = SponsorListingCreationModel.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    profile.sponsors_u_ordered.add(listing)

    buyer = request.user
    buyer_profile = Profile.objects.get(user=buyer)
    buyers_sponsor_listings = buyer.sponsorlistingcreationmodel_set.all()
    buyers_creator_listings = buyer.bloglistingcreationmodel_set.all()

    creator = listing.creator

    prev_s_order = None

    try:
        prev_s_order = SponsorOrderModel.objects.get(buyer=buyer, sponsor_listing=listing)
    except:
        prev_s_order = None

    if (request.method == 'POST'):
        # add instance field for updating -> , instance=prev_c_order
        form = SponsorOrderForm(request.POST, instance=prev_s_order)

        if (form.is_valid()):
            obj = form.save(commit=False)

            obj.buyer = buyer
            obj.creator = creator
            obj.sponsor_listing = listing

            buyer_listing = form.cleaned_data['buyer_listing']
            creator_l = BlogListingCreationModel.objects.all()
            sponsor_l = SponsorListingCreationModel.objects.all()

            for l in creator_l:
                if (str(l) == str(buyer_listing)):
                    obj.buyers_listing_c = l

            for l in sponsor_l:
                if (str(l) == str(buyer_listing)):
                    obj.buyers_listing_s = l

            obj.save()
            print('---------- order was saved -----------')

        return redirect(reverse('sponsor_marketplace_listing_view', kwargs={'id': listing.id}))

    context = {
        'buyer': buyer,
        'creator': creator,
        'buyers_sponsor_listings': buyers_sponsor_listings,
        'buyers_creator_listings': buyers_creator_listings,
        'prev_s_order': prev_s_order
    }

    return render(request, 'sponsor_marketplace_listing_order_detail_view.html', context)
    # return redirect(reverse('creator_marketplace_listing_view', kwargs={'id': listing.id}))



def sponsor_marketplace_listing_unorder_view(request, id=None):
    marketplace_s_listing = SponsorListingCreationModel.objects.get(id=id)
    current_users_profile = Profile.objects.get(user=request.user)
    sponsor_order = SponsorOrderModel.objects.get(buyer=request.user, sponsor_listing=marketplace_s_listing)

    sponsor_order.delete()
    current_users_profile.sponsors_u_ordered.remove(marketplace_s_listing)
    return redirect(reverse('sponsor_marketplace_listing_view', kwargs={'id': marketplace_s_listing.id}))
