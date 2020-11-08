from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .decorators import user_is_entry_author

from .models import SponsorListingCreationModel
from .forms import SponsorListingCreationForm
from users.models import Profile

@login_required(login_url='login')
def sponsor_listing_creation(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    notification_types = [

        'Initial',
        'Accepted',
        'Escrow',
        'Completed'

    ]

    context = {
        'notification_types': notification_types,
    }

    if request.method == 'POST':
        form = SponsorListingCreationForm(request.POST or None)

        if form.is_valid():
            form.save(commit=False).creator = request.user
            form.save(commit=False).notification_type = request.POST.getlist('notification_types')
            form.save()

            return redirect('home')

    return render(request, 'sponsor_listing_creation.html', context)


@login_required(login_url='login')
def sponsor_listing_creation_type_s(request):

    user = request.user
    profile = Profile.objects.get(user=user)

    profile.type = 'sponsor'
    profile.save()

    return redirect('sponsor_listing')


@login_required(login_url='login')
@user_is_entry_author
def sponsor_listing_update(request, id=None):
    listing = SponsorListingCreationModel.objects.get(id=id)

    notification_types = [

        'Initial',
        'Accepted',
        'Escrow',
        'Completed'

    ]


    context = {
        'listing':listing,
        'notification_types': notification_types,
    }
    if request.method == 'POST':
        form = SponsorListingCreationForm(request.POST,request.FILES, instance=listing)
        if form.is_valid():
            form.save(commit=False).notification_type = request.POST.getlist('notification_types')
            form.save()

        return redirect('home')
    return render(request, 'sponsor_listing_creation.html', context)

@login_required(login_url='login')
@user_is_entry_author
def sponsor_listing_delete(request, id=None):
    listing = SponsorListingCreationModel.objects.get(id=id)
    context = {
        'listing':listing
    }
    listing.delete()

    return redirect('dashboard')
