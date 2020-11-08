from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import SponsorListingCreationModel
from .forms import SponsorListingCreationForm
from users.models import Profile

@login_required(login_url='login')
def sponsor_listing_creation(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    if request.method == 'POST':
        form = SponsorListingCreationForm(request.POST or None)

        if form.is_valid():
            form.save(commit=False).creator = request.user
            form.save()

            return redirect('home')

    return render(request, 'sponsor_listing_creation.html')


@login_required(login_url='login')
def sponsor_listing_creation_type_s(request):

    user = request.user
    profile = Profile.objects.get(user=user)

    profile.type = 'sponsor'
    profile.save()

    return redirect('sponsor_listing')


@login_required(login_url='login')
def sponsor_listing_update(request, id=None):
    listing = SponsorListingCreationModel.objects.get(id=id)
    context = {
        'listing':listing
    }
    if request.method == 'POST':
        form = SponsorListingCreationForm(request.POST,request.FILES, instance=listing)
        if form.is_valid():
            form.save()

        return redirect('home')
    return render(request, 'sponsor_listing_creation.html', context)

@login_required(login_url='login')
def sponsor_listing_delete(request, id=None):
    listing = SponsorListingCreationModel.objects.get(id=id)
    context = {
        'listing':listing
    }
    listing.delete()

    return redirect('dashboard')
