from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from creator_listings.models import BlogListingCreationModel
from sponsor_listings.models import SponsorListingCreationModel
from users.models import Profile, CreatorOrderModel, SponsorOrderModel, Messages
from users.forms import CreatorOrderForm, SponsorOrderForm
from .filters import CreatorListingFilter, SponsorListingFilter


#
#  Self defined functions
#

def search_query_kw(list):
    keywords = list[0]
    new_list = keywords.split(" ")
    return new_list


#
# Creator Listing Stuff
#

# The creator marketplace page
def creator_marketplace(request):
    creator_listings = BlogListingCreationModel.objects.all()

    # Returns a list of all the names of the input tags that have been checked
    niche_query = request.GET.getlist('niche')
    lang_query = request.GET.getlist('language')
    searchbar_keywords = request.GET.getlist('search_bar')
    blog_age_val = request.GET.get('blog_age_val')
    searchb = request.GET.get('search_bar')
    reset_button = request.GET.get('reset_button')
    searchbar_bool = False

    if reset_button:
        print('reset')
        return redirect('creator_marketplace')

    if blog_age_val is None:
        blog_age_val = 0

    creator_listings = creator_listings.filter(age__gt=blog_age_val)

    niches = {
        "Apparel & Accessories": "",
        "Arts & Crafts": "",
        "Autos & Vehicles": "",
        "Baby & Children Products": "",
        "Beauty & Personal Care": "",
        "Business & Industrial": "",
        "Educational": "",
        "Food": "",
        "Home & Garden": "",
        "Lifestyle": "",
        "Media & Entertainment": "",
        "Sports & Fitness": "",
        "Travel": "",
        "Technology": "",
        "Other": ""
        }

    for niche in niche_query:
        if niche in niche_query:
            niches[str(niche)] = "checked"
        else:
            niches[str(niche)] = ""

    if niche_query != "" and niche_query is not None and len(niche_query) != 0:
        creator_listings = creator_listings.filter(niche__in=niche_query)

    langs = {
        "English": "",
        "Spanish": "",
        "Chinese": "",
        "Other": ""
        }

    for l in lang_query:
        if l in lang_query:
            langs[str(l)] = "checked"
        else:
            langs[str(l)] = ""

    if lang_query != "" and lang_query is not None and len(lang_query) != 0:
        creator_listings = creator_listings.filter(language__in=lang_query)


    if searchbar_keywords and search_query_kw(searchbar_keywords)[0] != '':
        searchbar_bool = True

        keywords = search_query_kw(searchbar_keywords)

        creator_listing_ids = []

        for keyword in keywords:
            listings = creator_listings.filter(search_keywords__icontains=keyword)
            for l in listings:
                creator_listing_ids.append(l.id)

        creator_listings = creator_listings.filter(id__in=creator_listing_ids)


    watching = []

    if (request.user.is_authenticated):
        profile = Profile.objects.get(user=request.user)


        for listing in creator_listings:
            if (listing in profile.creators_watched.all()):
                watching.append(listing)


    context = {
        'creator_listings': creator_listings,
        'niches': niches,
        'langs': langs,
        'watching': watching,
        'blog_age_val': blog_age_val,
        'searchb': searchb,
        'searchbar_bool': searchbar_bool
        #'c_listing_filter': c_listing_filter,
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
    all_users_listings = BlogListingCreationModel.objects.filter(creator=listing.creator)

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
        'ordered': ordered,
        'all_users_listings': all_users_listings
    }

    return render(request, 'creator_marketplace_listing_view.html', context)

##### watching #####

# The logic for watching and unwatching a listing
'''
def creator_marketplace_watch_view(request, id=None):
    listing = BlogListingCreationModel.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    profile.creators_watched.add(listing)
    return redirect('creator_marketplace')
'''

@login_required(login_url='login')
def creator_marketplace_listing_watch_view(request, id=None):
    listing = BlogListingCreationModel.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    profile.creators_watched.add(listing)

    return redirect(reverse('creator_marketplace_listing_view', kwargs={'id': listing.id}))

@login_required(login_url='login')
def creator_marketplace_listing_unwatch_view(request, id=None):
    listing = BlogListingCreationModel.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    profile.creators_watched.remove(listing)

    messages.success(request, "%s has been removed from watchlist" % (listing.blog_name))

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

    # not neccessary
    buyers_creator_listings = buyer.bloglistingcreationmodel_set.all()

    creator = listing.creator

    prev_c_order = None

    try:
        prev_c_order = CreatorOrderModel.objects.get(buyer=buyer, creator_listing=listing)
    except:
        prev_c_order = None



    if (request.method == 'POST'):
        # add instance field for updating -> , instance=prev_c_order
        form = CreatorOrderForm(request.POST, request.FILES, instance=prev_c_order)

        if (form.is_valid()):
            obj = form.save(commit=False)

            obj.buyer = buyer
            obj.creator = creator
            obj.creator_listing = listing
            obj.payout = form.cleaned_data['payout']
            obj.s_content_file = form.cleaned_data['s_content_file']


            buyer_listing = form.cleaned_data['buyer_listing']
            creator_l = BlogListingCreationModel.objects.all()
            sponsor_l = SponsorListingCreationModel.objects.all()

            for l in creator_l:
                if (str(l) == str(buyer_listing)):
                    obj.buyers_listing_c = l

            for l in sponsor_l:
                if (str(l) == str(buyer_listing)):
                    obj.buyers_listing_s = l

            Messages.objects.create(sender=buyer, reciever=listing.creator, message="%s has been ordered by %s" % (listing.blog_name, buyer_listing))
            messages.success(request, "%s has been successfully ordered" % (listing.blog_name), extra_tags="sponsor_orders_creator_success")

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

    Messages.objects.create(sender=creator_order.buyer, reciever=creator_order.creator, message="%s has been unordered by %s" % (creator_order.creator_listing.blog_name, creator_order.buyers_listing_s.product))
    messages.success(request, "%s has been successfully unordered" % (creator_order.creator_listing.blog_name), extra_tags="sponsor_unorders_creator_success")

    creator_order.delete()
    current_users_profile.creators_u_ordered.remove(marketplace_c_listing)
    return redirect(reverse('creator_marketplace_listing_view', kwargs={'id': marketplace_c_listing.id}))


#
# Sponsor Listing Stuff
#

# The sponsor marketplace page
def sponsor_marketplace(request):
    sponsor_listings = SponsorListingCreationModel.objects.all()

    niche_query = request.GET.getlist('niche')
    lang_query = request.GET.getlist('language')
    searchbar_keywords = request.GET.getlist('search_bar')
    searchb = request.GET.get('search_bar')
    reset_button = request.GET.get('reset_button')
    searchbar_bool = False

    niches = {
        "Apparel & Accessories": "",
        "Arts & Crafts": "",
        "Autos & Vehicles": "",
        "Baby & Children Products": "",
        "Beauty & Personal Care": "",
        "Business & Industrial": "",
        "Educational": "",
        "Food": "",
        "Home & Garden": "",
        "Lifestyle": "",
        "Media & Entertainment": "",
        "Sports & Fitness": "",
        "Travel": "",
        "Technology": "",
        "Other": ""
        }

    for niche in niche_query:
        if niche in niche_query:
            niches[str(niche)] = "checked"
        else:
            niches[str(niche)] = ""

    if niche_query != "" and niche_query is not None and len(niche_query) != 0:
        sponsor_listings = sponsor_listings.filter(niche__in=niche_query)

    langs = {
        "English": "",
        "Spanish": "",
        "Chinese": "",
        "Other": ""
        }

    for l in lang_query:
        if l in lang_query:
            langs[str(l)] = "checked"
        else:
            langs[str(l)] = ""

    if lang_query != "" and lang_query is not None and len(lang_query) != 0:
        sponsor_listings = sponsor_listings.filter(language__in=lang_query)

    if searchbar_keywords and search_query_kw(searchbar_keywords)[0] != '':
        searchbar_bool = True

        keywords = search_query_kw(searchbar_keywords)

        sponsor_listings_ids = []

        for keyword in keywords:
            listings = sponsor_listings.filter(search_keywords__icontains=keyword)
            for l in listings:
                sponsor_listings_ids.append(l.id)

        sponsor_listings = sponsor_listings.filter(id__in=sponsor_listings_ids)

    watching = []

    if (request.user.is_authenticated):
        profile = Profile.objects.get(user=request.user)

        for listing in sponsor_listings:
            if (listing in profile.sponsors_watched.all()):
                watching.append(listing)

    context = {
        'sponsor_listings': sponsor_listings,
        'niches': niches,
        'watching': watching,
        'langs': langs,
        'searchbar_bool': searchbar_bool,
        'searchb': searchb
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

    all_users_listings = SponsorListingCreationModel.objects.filter(creator=listing.creator)

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
        'ordered': ordered,
        'all_users_listings': all_users_listings
    }

    return render(request, 'sponsor_marketplace_listing_view.html', context)

##### watching #####

# The logic for watching and unwatching a listing

@login_required(login_url='login')
def sponsor_marketplace_listing_watch_view(request, id=None):
    listing = SponsorListingCreationModel.objects.get(id=id)
    profile = Profile.objects.get(user=request.user)
    profile.sponsors_watched.add(listing)
    return redirect(reverse('sponsor_marketplace_listing_view', kwargs={'id': listing.id}))

@login_required(login_url='login')
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

            Messages.objects.create(sender=buyer, reciever=listing.creator, message="%s has been ordered by %s" % (listing.product, buyer_listing))
            messages.success(request, "%s has been successfully ordered" % (listing.product), extra_tags="creator_orders_sponsor_success")

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

    Messages.objects.create(sender=sponsor_order.buyer, reciever=sponsor_order.creator, message="%s has been unordered by %s" % (sponsor_order.sponsor_listing.product, sponsor_order.buyers_listing_c.blog_name))
    messages.success(request, "%s has been successfully unordered" % (sponsor_order.sponsor_listing.product), extra_tags="creator_unorders_sponsor_success")

    return redirect(reverse('sponsor_marketplace_listing_view', kwargs={'id': marketplace_s_listing.id}))
