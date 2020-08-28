from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from django.contrib.auth.forms import UserCreationForm
from .models import Profile, CreatorOrderModel, SponsorOrderModel
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
    
    for i in c_orders:
        print('---------------------')
        print(i.buyers_listing_s)

    c_ordered = profile.creators_u_ordered.all()
    s_ordered = profile.sponsors_u_ordered.all()


    #The created listings of each type (creator and sponsor), if they created any
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

def dashboard_creator_order_accept(request, id=None):
    return redirect('dashboard')

def dashboard_creator_order_decline(request, id=None):
    return redirect('dashboard')