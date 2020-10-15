from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm
from .models import (Profile, CreatorOrderModel, SponsorOrderModel, AcceptedCreatorOrderModel, AcceptedSponsorOrderModel,
CompletedOrderModel)

from creator_listings.models import BlogListingCreationModel
from sponsor_listings.models import SponsorListingCreationModel
from django.contrib.auth.models import User
from .forms import CreatorOrderForm, SupportTicketForm, FeatureTicketForm, SponsorEditForm, SponsorReviewForm


def account(request, id=None):
    user = User.objects.get(username=request.user.username)

    personal_c_pending_listings = len(CreatorOrderModel.objects.filter(creator=user))
    personal_s_pending_listings = len(SponsorOrderModel.objects.filter(creator=user))
    personal_caccepted_listings = len(AcceptedCreatorOrderModel.objects.filter(creator=user))
    personal_saccepted_listings = len(AcceptedSponsorOrderModel.objects.filter(creator=user))
    personal_completed = len(CompletedOrderModel.objects.filter(creator=user))

    personal_creator_listings = user.bloglistingcreationmodel_set.all()
    personal_sponsor_listings = user.sponsorlistingcreationmodel_set.all()

    i = 0
    ic = 0
    is_ = 0
    for l in personal_creator_listings:
        i += 1
        ic += 1

    for l in personal_sponsor_listings:
        i += 1
        is_ += 1

    ip = 0
    ia = 0
    ic = 0

    context = {
        'personal_c_listings': personal_creator_listings,
        'personal_s_listings': personal_sponsor_listings,
        'num_of_c_listings': ic,
        'num_of_s_listings': is_,
        'num_of_total_listings': i,
        'num_of_cp_listings': personal_c_pending_listings,
        'num_of_sp_listings': personal_s_pending_listings,
        'num_of_ca_listings': personal_caccepted_listings,
        'num_of_ca_listings': personal_saccepted_listings,
        'num_of_completed_listings': personal_completed,
    }

    return render(request, 'account.html', context)

def delete_account(request):
    user = User.objects.get(username=request.user.username)
    user.delete()

    return redirect('home')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'User Created For: ' + user)

            return redirect('login')
            messages.info(request, 'Invalid Input For Password')
        context = {
            'form': form,
        }
        return render(request, 'signup.html', context)

    else:
        form = CustomUserCreationForm(request.POST)
        context = {
            'form': form,
        }
        return render(request, 'signup.html', context)

def support_contact(request):
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)

        if form.is_valid():
            form.save(commit=False).creator = request.user
            form.save()

            return redirect('home')

    return render(request, 'support.html')

def feature_add(request):
    if request.method == 'POST':

        form = FeatureTicketForm(request.POST)

        if form.is_valid():

            form.save(commit=False).creator = request.user
            form.save()

            return redirect('home')

    return render(request, 'feature.html')

@login_required(login_url='login')
def dashboard(request):
    user = User.objects.get(username=request.user.username) # current logged in user
    profile = Profile.objects.get(user=user) # current logged in users Profile

    c_watching = profile.creators_watched.all()
    s_watching = profile.sponsors_watched.all()

    c_watch_len = c_watching.count()
    s_watch_len = s_watching.count()
    total_watch_len = c_watch_len + s_watch_len

    # The logged in users creator listings
    c_orders = CreatorOrderModel.objects.filter(creator=user)
    c_orders_len = c_orders.count()

    # The logged in users sponsor listings
    s_orders = SponsorOrderModel.objects.filter(creator=user)
    s_orders_len = s_orders.count()

    # The creator and sponsor ORDERS the logged in user has made
    c_ordered = CreatorOrderModel.objects.filter(buyer=user) # profile.creators_u_ordered.all()
    c_ordered_len = c_ordered.count()
    s_ordered = SponsorOrderModel.objects.filter(buyer=user) # profile.sponsors_u_ordered.all()
    s_ordered_len = s_ordered.count()

    # The ACCEPTED creator and sponsor ORDERS the logged in user has made
    accepted_c_orders = AcceptedCreatorOrderModel.objects.filter(buyer=user)

    # The COMPLETED creator and sponsor ORDERS the logged in user has made
    completed_c_orders = CompletedOrderModel.objects.filter(creator=user)

    # The orders that the logged in user has made
    c_accepted_orders = AcceptedCreatorOrderModel.objects.filter(creator=user)
    c_accepted_orders_len = c_accepted_orders.count()
    s_accepted_orders = AcceptedSponsorOrderModel.objects.filter(creator=user)
    s_accepted_orders_len = s_accepted_orders.count()

    # The created listings of each type (creator and sponsor), if they created any
    personal_creator_listings = user.bloglistingcreationmodel_set.all()
    p_c_listing_len = personal_creator_listings.count()
    personal_sponsor_listings = user.sponsorlistingcreationmodel_set.all()
    p_s_listing_len = personal_sponsor_listings.count()


    context = {


        'personal_c_listings': personal_creator_listings,
        'personal_s_listings': personal_sponsor_listings,

        's_watching': s_watching,
        'c_watching': c_watching,

        'c_watch_len': c_watch_len,
        's_watch_len': s_watch_len,

        'total_watch_len': total_watch_len,

        's_ordered': s_ordered,
        'c_ordered': c_ordered,

        'c_ordered_len': c_ordered_len,
        's_ordered_len': s_ordered_len,

        's_orders': s_orders,
        's_orders_len': s_orders_len,
        'c_orders': c_orders,
        'c_orders_len': c_orders_len,

        'c_accepted_orders': c_accepted_orders,
        'c_accepted_orders_len': c_accepted_orders_len,
        's_accepted_orders': s_accepted_orders,
        's_accepted_orders_len': s_accepted_orders_len,

        'accepted_c_orders': accepted_c_orders,
        'completed_c_orders': completed_c_orders,

        'total_orders_num': (c_orders_len + s_orders_len),
        'total_acc_orders_num': (c_accepted_orders_len + s_accepted_orders_len),

        'p_c_listing_len': p_c_listing_len,
        'p_s_listing_len': p_s_listing_len,

        'total_listings_num': (p_c_listing_len + p_s_listing_len),

        'profile': profile,
    }

    return render(request, 'dashboard.html', context)


def dashboard_send_review(request, id=None):
    # 1. This is for the creator to send over the content they made to the sponsor
    #    so they can view it and approve it.
    # 2. There'll be form stuff here so the content the creator adds to this url
    #    is saved in the DB, so it can then be displayed to the sponsor in the
    #    "Creators To Review" section in the dashboard.

    listing = AcceptedCreatorOrderModel.objects.get(id=id)
    turn = listing.turn

    if(request.method == 'POST'):

        form = SponsorReviewForm(request.POST)

        if form.is_valid():
            file = form.cleaned_data.get('review_file')
            listing.review_file = file
            listing.turn = 's'
            listing.save()

            return redirect('dashboard')


    content = {
        'listing': listing,
    }


    return render(request, 'send_review.html')

def dashboard_s_acc(request, id=None):
    # 1. Make "sponsor_change" = None in the DB for this specific order.
    # 2. Do logic to put this order back in the "Sponsor Accepted Orders" tab,
    #    and in the tamplate there's logic for displaying the right buttons
    # 3. Add escrow.com script here for the sponsor.
    listing = AcceptedCreatorOrderModel.objects.get(id=id)

    listing.turn = 'c'

    listing.sponsor_approves = True
    listing.status = 'Approved'
    listing.save()

    content = {
        'listing': listing,
    }
    return redirect('dashboard')

def dashboard_s_edit(request, id=None):
    # 1. There'll be form stuff here, and all this funciton is designed for is
    #    to add whatever edits the sponsor wants to make to the creators content

    listing = AcceptedCreatorOrderModel.objects.get(id=id)

    turn = listing.turn

    if(request.method == 'POST'):
        form = SponsorEditForm(request.POST)

        if form.is_valid():
            edit = form.cleaned_data.get('edits')
            listing.edits = edit
            listing.turn = 'c'
            listing.save()

            return redirect('dashboard')


    content = {
        'listing': listing,
    }

    return render(request, 's_edit.html', content)

#
# Watch and unwatch feature on dashboard
#

def dashboard_unwatch_c(request, id=None):
    users_profile = Profile.objects.get(user=request.user)
    listing = users_profile.creators_watched.get(id=id)
    users_profile.creators_watched.remove(listing)

    return redirect('dashboard')

def dashboard_unwatch_s(request, id=None):
    users_profile = Profile.objects.get(user=request.user)
    listing = users_profile.sponsors_watched.get(id=id)
    users_profile.sponsors_watched.remove(listing)

    return redirect('dashboard')

#
# Unordering creators and sponsors
#

def dashboard_unorder_c(request, id=None):
    users_profile = Profile.objects.get(user=request.user)
    listing = users_profile.creators_u_ordered.get(id=id)
    users_profile.creators_u_ordered.remove(listing)

    creator_order = CreatorOrderModel.objects.get(buyer=request.user, creator_listing=listing)
    creator_order.delete()

    return redirect('dashboard')

def dashbord_unorder_accepted_c(request, id=None):
    order = AcceptedCreatorOrderModel.objects.get(id=id)
    order.delete()
    return redirect('dashboard')


def dashboard_unorder_s(request, id=None):
    users_profile = Profile.objects.get(user=request.user)
    listing = users_profile.sponsors_u_ordered.get(id=id)
    users_profile.sponsors_u_ordered.remove(listing)

    sponsor_order = SponsorOrderModel.objects.get(buyer=request.user, sponsor_listing=listing)
    sponsor_order.delete()

    return redirect('dashboard')

#
# Accept and decline system on dashboard (for orders)
#
# Add functionality: send user an email that their order has been accepted or declined

def dashboard_creator_order_accept(request, id=None):

    try:
        #c_listing = BlogListingCreationModel.objects.get(id=id)
        c_order = CreatorOrderModel.objects.get(id=id)
        c_order.status = 'Accepted - In Process'

        c_order.save()

        # Accepted creator order (after creator clicks accept)
        ac_order = AcceptedCreatorOrderModel(
            buyer=c_order.buyer,
            creator=c_order.creator,
            creator_listing=c_order.creator_listing,
            buyer_listing=c_order.buyer_listing,
            buyers_listing_s=c_order.buyers_listing_s,
            buyers_listing_c=c_order.buyers_listing_c,
            service=c_order.service,
            service_detailed=c_order.service_detailed,
            status=c_order.status,
            who_initiated_order='sponsor',
            payout=c_order.payout,
            )

        ac_order.save()
        c_order.delete()

    except CreatorOrderModel.DoesNotExist:
        #s_listing = SponsorListingCreationModel.objects.get(id=id)
        s_order = SponsorOrderModel.objects.get(id=id)
        s_order.status = 'Accepted - In Process'

        s_order.save()

        # Accepted creator order (after creator clicks accept)
        as_order = AcceptedSponsorOrderModel(
            buyer=s_order.buyer,
            creator=s_order.creator,
            sponsor_listing=s_order.sponsor_listing,
            buyer_listing=s_order.buyer_listing,
            buyers_listing_s=s_order.buyers_listing_s,
            buyers_listing_c=s_order.buyers_listing_c,
            services_creator_is_willing_to_provide=s_order.services_creator_is_willing_to_provide,
            services_creator_is_willing_to_provide_detailed=s_order.services_creator_is_willing_to_provide_detailed,
            status=s_order.status

        )

        as_order.save()
        s_order.delete()


    return redirect('dashboard')

def dashboard_creator_order_decline(request, id=None):
    try:
        c_order = CreatorOrderModel.objects.get(id=id)
        c_order.status = 'Declined'

        c_order.delete()

    except CreatorOrderModel.DoesNotExist:
        s_order = SponsorOrderModel.objects.get(id=id)
        s_order.status = 'Declined'

        s_order.delete()

    return redirect('dashboard')


def dashboard_sponsor_order_accept(request, id=None):

    order = SponsorOrderModel.objects.get(id=id)

    creator_listing = BlogListingCreationModel.objects.get(id=order.buyers_listing_c.id)
    profile = Profile.objects.get(user=request.user)

    profile.creators_u_ordered.add(creator_listing)

    buyer = request.user
    buyer_profile = Profile.objects.get(user=buyer)
    buyers_sponsor_listings = buyer.sponsorlistingcreationmodel_set.all()
    buyers_creator_listings = buyer.bloglistingcreationmodel_set.all()

    creator = creator_listing.creator

    if (request.method == 'POST'):
        # add instance field for updating -> , instance=prev_c_order
        form = CreatorOrderForm(request.POST or None)

        if (form.is_valid()):
            obj = form.save(commit=False)
            obj.payout = form.cleaned_data['payout']

            order.status = 'Accepted - In Process'

            order.save()

            # Accepted creator order (after creator clicks accept)



            ac_order = AcceptedCreatorOrderModel(
                buyer=request.user,
                creator=creator_listing.creator,
                creator_listing=creator_listing,
                buyer_listing=order.sponsor_listing,
                buyers_listing_s=order.sponsor_listing,

                service=obj.service,
                service_detailed=obj.service_detailed,

                status='Accepted - In Progress',
                who_initiated_order = 'creator',
                payout = obj.payout,
                )

            ac_order.save()
            order.delete()

            #obj.save()

            return redirect('dashboard')


    return render(request, 'acceptedcreator.html')

def dashboard_sponsor_order_decline(request, id=None):

    try:
        #c_listing = BlogListingCreationModel.objects.get(id=id)
        c_order = CreatorOrderModel.objects.get(id=id)
        c_order.status = 'Declined'

        c_order.delete()

    except CreatorOrderModel.DoesNotExist:
        #s_listing = SponsorListingCreationModel.objects.get(id=id)
        s_order = SponsorOrderModel.objects.get(id=id)
        s_order.status = 'Declined'

        s_order.delete()

    return redirect('dashboard')


def dashboard_creator_order_complete(request, id=None):
    order = AcceptedCreatorOrderModel.objects.get(id=id)
    order.status = 'complete'
    order.save()


    try:
        #c_listing = BlogListingCreationModel.objects.get(id=id)
        c_order = AcceptedCreatorOrderModel.objects.get(id=id)
        c_order.status = 'Complete'

        c_order.save()

        # Accepted creator order (after creator clicks accept)
        cc_order = CompletedOrderModel(
            buyer=c_order.buyer,
            creator=c_order.creator,
            creator_listing=c_order.creator_listing,
            buyer_listing=c_order.buyer_listing,
            buyers_listing_s=c_order.buyers_listing_s,
            buyers_listing_c=c_order.buyers_listing_c,
            service=c_order.service,
            service_detailed=c_order.service_detailed,
            status=c_order.status,
            who_initiated_order=c_order.who_initiated_order,
            payout=c_order.payout
            )

        cc_order.save()
        c_order.delete()

    #This should probably be removed and has no functions
    except CreatorOrderModel.DoesNotExist:
        #s_listing = SponsorListingCreationModel.objects.get(id=id)
        s_order = SponsorOrderModel.objects.get(id=id)
        s_order.status = 'Accepted - In Process'

        s_order.save()

        # Accepted creator order (after creator clicks accept)
        as_order = AcceptedSponsorOrderModel(
            buyer=s_order.buyer,
            creator=s_order.creator,
            sponsor_listing=s_order.sponsor_listing,
            buyer_listing=s_order.buyer_listing,
            buyers_listing_s=s_order.buyers_listing_s,
            buyers_listing_c=s_order.buyers_listing_c,
            services_creator_is_willing_to_provide=s_order.services_creator_is_willing_to_provide,
            services_creator_is_willing_to_provide_detailed=s_order.services_creator_is_willing_to_provide_detailed,
            status=s_order.status

        )

        as_order.save()
        s_order.delete()

    return redirect('dashboard')

def dashboard_sponsor_order_complete(request, id=None):

    order = AcceptedSponsorOrderModel.objects.get(id=id)
    order.status = 'complete'
    order.save()

    return redirect('dashboard')

def dashboard_withdraw_order(request, id=None):
    order = AcceptedCreatorOrderModel.objects.get(id=id)
    order.delete()

    return redirect('dashboard')
