from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from django.contrib.auth.forms import UserCreationForm
from .models import Profile, CreatorOrderModel, SponsorOrderModel,AcceptedCreatorOrderModel, AcceptedSponsorOrderModel, CompletedOrderModel
from creator_listings.models import BlogListingCreationModel
from sponsor_listings.models import SponsorListingCreationModel
from django.contrib.auth.models import User


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('home')
    else:
        form = UserCreationForm(request.POST)
        context = {
            'form': form,
        }
        return render(request, 'signup.html', context)



def dashboard(request):
    user = User.objects.get(username=request.user.username) # current logged in user
    profile = Profile.objects.get(user=user) # current logged in users Profile
    
    c_watching = profile.creators_watched.all()
    s_watching = profile.sponsors_watched.all()

    c_orders = CreatorOrderModel.objects.filter(creator=user)
    c_orders_len = c_orders.count()

    s_orders = SponsorOrderModel.objects.filter(creator=user)
    s_orders_len = s_orders.count()

    c_ordered = CreatorOrderModel.objects.filter(buyer=user) # profile.creators_u_ordered.all()
    s_ordered = SponsorOrderModel.objects.filter(buyer=user) # profile.sponsors_u_ordered.all()

    c_accepted_orders = AcceptedCreatorOrderModel.objects.filter(creator=user)
    c_accepted_orders_len = c_accepted_orders.count()
    s_accepted_orders = AcceptedSponsorOrderModel.objects.filter(creator=user)
    s_accepted_orders_len = s_accepted_orders.count()

    # c_order_status = CreatorOrderModel.objects.filter(buyer=user)

    # The created listings of each type (creator and sponsor), if they created any
    personal_creator_listings = user.bloglistingcreationmodel_set.all()
    personal_sponsor_listings = user.sponsorlistingcreationmodel_set.all()

    context = {
        'personal_c_listings': personal_creator_listings,
        'personal_s_listings': personal_sponsor_listings,

        's_watching': s_watching,
        'c_watching': c_watching,

        's_ordered': s_ordered,
        'c_ordered': c_ordered,

        's_orders': s_orders,
        's_orders_len': s_orders_len,
        'c_orders': c_orders,
        'c_orders_len': c_orders_len,

        'c_accepted_orders': c_accepted_orders,
        'c_accepted_orders_len': c_accepted_orders_len,
        's_accepted_orders': s_accepted_orders,
        's_accepted_orders_len': s_accepted_orders_len,

        'profile': profile,
    }

    return render(request, 'dashboard.html', context)

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
            status=c_order.status
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
            status=c_order.status
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
            status=c_order.status
            )

        cc_order.save()
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


def dashboard_sponsor_order_complete(request, id=None):
    order = AcceptedSponsorOrderModel.objects.get(id=id)
    order.status = 'complete'
    order.save()

    return redirect('dashboard')

def dashboard_withdraw_order(request, id=None):
    order = AcceptedCreatorOrderModel.objects.get(id=id)
    order.delete()

    return redirect('dashboard')