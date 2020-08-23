from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SponsorListingCreationModel
from .forms import SponsorListingCreationForm

def sponsor_listing_creation(request):
    if request.method == 'POST':
        form = SponsorListingCreationForm(request.POST or None)
        if form.is_valid():
            form.save(commit=False).creator = request.user
            form.save()

            return redirect('home')
        
        '''if (id):
            listing = SponsorListingCreationModel.objects.get(id=id)
            context = {
                'listing': listing
            }

            return render(request, 'sponsor_listing_creation.html', context)'''
    return render(request, 'sponsor_listing_creation.html')


def sponsor_listing_update(request, id=None):
    listing = SponsorListingCreationModel.objects.get(id=id)
    context = {
        'listing':listing
    }
    if request.method == 'POST':
        form = SponsorListingCreationForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()

        return redirect('home')
    return render(request, 'sponsor_listing_creation.html', context) 


def sponsor_listing_delete(request, id=None):
    listing = SponsorListingCreationModel.objects.get(id=id)
    context = {
        'listing':listing
    }
    listing.delete()

    return redirect('dashboard')
    