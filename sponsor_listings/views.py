from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .decorators import user_is_entry_author

import os

from .models import SponsorListingCreationModel
from .forms import SponsorListingCreationForm
from users.models import Profile

@login_required(login_url='login')
def sponsor_listing_creation(request):
    user = request.user
    profile = Profile.objects.get(user=user)

    notification_types = [

        'Listing is Ordered',
        'Listing is Unordered',
        'Order is Accepted by Creator',
        'Order is Declined by Creator',
        'Creator has Sent Content for Review',
        'Creator has Withdrawn from Accepted Order',
        'Creator Sends Content URL'

    ]

    context = {
        'notification_types': notification_types,
    }

    if request.method == 'POST':
        form = SponsorListingCreationForm(request.POST or None)

        if form.is_valid():
            form.save(commit=False).creator = request.user
            form.save(commit=False).notification_type = request.POST.getlist('notification_types')

            name = form.cleaned_data['product']

            form.save()

            messages.success(request, "%s has been successfully created." % (name), extra_tags="sponsor_listing_creation")

            return redirect('home')

        elif form.errors:

            messages.error(request, "There was an error. A common issue is that you need to select an image file for you listing image.", extra_tags="sponsor_listing_creation_error")

            return redirect('sponsor_listing')

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

    img_path = os.path.basename(listing.listing_img.path)
    i = img_path.rfind('_')
    img_file_name = img_path[:i] + img_path[i+8:]


    notification_types = [

        'Listing is Ordered',
        'Listing is Unordered',
        'Order is Accepted by Sponsor',
        'Order is Declined by Sponsor',
        'Sponsor has Sent Edits for Accepted Order',
        'Sponsor has initiated Escrow Process'

    ]

    update_bool = "True"


    context = {
        'listing':listing,
        'notification_types': notification_types,
        'update_bool': update_bool,
        'img_file_name': img_file_name,
    }

    if(listing.search_keywords):
        original_string = listing.search_keywords
        characters_to_remove = "[]'"

        new_string = original_string
        for character in characters_to_remove:
            new_string = new_string.replace(character, "")

        kw = new_string.split()
        search_kw = " ".join(kw)

        context['search_kw'] = search_kw

    if request.method == 'POST':
        form = SponsorListingCreationForm(request.POST,request.FILES, instance=listing)
        if form.is_valid():
            form.save(commit=False).notification_type_email = request.POST.getlist('notification_type_email')
            form.save(commit=False).notification_type_phone = request.POST.getlist('notification_type_phone')
            form.save()

            messages.success(request, "%s has been successfully updated." % (listing.product), extra_tags="sponsor_listing_update")

        elif form.errors:

            messages.error(request, "There was an error - %s." % (str(form.errors)), extra_tags="sponsor_listing_update_error")
            print('------', form.errors)

            return redirect(reverse('sponsor_listing_update', kwargs={'id': listing.id}))

        return redirect('home')
    return render(request, 'sponsor_listing_creation.html', context)

@login_required(login_url='login')
@user_is_entry_author
def sponsor_listing_delete(request, id=None):
    listing = SponsorListingCreationModel.objects.get(id=id)

    messages.success(request, "%s has been successfully deleted." % (listing.product), extra_tags="sponsor_listing_deleted")

    context = {
        'listing':listing
    }
    listing.delete()

    return redirect('dashboard')
