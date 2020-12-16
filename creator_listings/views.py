from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .decorators import user_is_entry_author

import os

from .models import BlogListingCreationModel
from users.models import Profile
from .forms import BlogListingCreationForm

from users.functions.csv_parser import csv_parser

@login_required(login_url='login')
def blogger_listing_creation(request):
    type_query = request.POST.getlist('blog_type')
    user = request.user
    profile = Profile.objects.get(user=user)

    #if(profile.type == 'none'):
        #return redirect('dashboard')


    types = [
        'Review',
        'Informative',
        'Discussion',
        'Tutorial',
        'Other',
    ]


    notification_types = [

        'Listing is Ordered',
        'Listing is Unordered',
        'Order is Accepted by Sponsor',
        'Order is Declined by Sponsor',
        'Sponsor has Sent Edits for Accepted Order',
        'Sponsor has initiated Escrow Process',
        'Sponsor Claims Content URL is Invalid',
        'Sponsor Has Marked Order as Complete'

    ]


    context = {
        'types': types,
        'notification_types': notification_types,
        'profile': profile,
    }

    if request.method == 'POST':
        form = BlogListingCreationForm(request.POST, request.FILES)


        if form.is_valid():
            form.save(commit=False).creator = request.user
            form.save(commit=False).blog_type = type_query

            form.save(commit=False).notification_type = request.POST.getlist('notification_types')
            form.save(commit=False).blog_type = request.POST.getlist('types')

            name = form.cleaned_data['blog_name']

            kw = form.cleaned_data['search_keywords']
            form.save(commit=False).search_keywords = kw #.split(", ")

            csv_file = form.cleaned_data['google_a_csv']

            if(csv_file is not None):
                f = csv_file

                is_google_a_data_good = csv_parser(f)

                if(is_google_a_data_good != None):
                    is_google_a_data_good = True

                    data, total_views, year, months = csv_parser(open(csv_file.path))

                else:
                    is_google_a_data_good = False

                if is_google_a_data_good:
                    avg_views = 0
                    for counter, l in enumerate(data):
                        if counter != 1 or 13:
                            avg_views = avg_views + l[1]

                    avg_views = int(avg_views/12)

                    form.save(commit=False).monthly_views = avg_views

                form.save()

            messages.success(request, "%s has been successfully created." % (name), extra_tags="blog_listing_creation")

        return redirect('home')

    return render(request, 'blog_listing_creation.html', context)

@login_required(login_url='login')
def creator_listing_creation_type_c(request):

    user = request.user
    profile = Profile.objects.get(user=user)

    profile.type = 'creator'
    profile.save()

    return redirect('blog_listing')


@login_required(login_url='login')
@user_is_entry_author
def blogger_listing_update(request, id=None):
    listing = BlogListingCreationModel.objects.get(id=id)

    img_path = os.path.basename(listing.listing_img.path)
    i = img_path.rfind('_')
    img_file_name = img_path[:i] + img_path[i+8:]

    types = [
        'Review',
        'Informative',
        'Discussion',
        'Tutorial',
        'Other',
    ]

    notification_types = [

        'Listing is Ordered',
        'Listing is Unordered',
        'Order is Accepted by Sponsor',
        'Order is Declined by Sponsor',
        'Sponsor Has Sent Edits For Accepted Order',
        'Sponsor Has Initiated Escrow Process',
        'Sponsor Claims Content URL is Invalid',
        'Sponsor Has Marked Order as Complete'

    ]

    n_types_e = listing.notification_type_email.strip('][').replace('\'', '').split(', ')


    n_types_m = listing.notification_type_phone.strip('][').replace('\'', '').split(', ')


    update_bool = "True"


    context = {
        'listing':listing,
        'types':types,
        'notification_types': notification_types,
        'update_bool': update_bool,
        'img_file_name': img_file_name,
        'n_types_e': n_types_e,
        'n_types_m': n_types_m
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

    if(listing.google_a_csv):
        ga_file_path = os.path.basename(listing.google_a_csv.name)

        i = ga_file_path.rfind('_')
        ga_file_name = ga_file_path[:i] + ga_file_path[i+8:]

        context['ga_file_name'] = ga_file_name

    if request.method == 'POST':
        form = BlogListingCreationForm(request.POST,request.FILES, instance=listing)
        if form.is_valid():
            form.save(commit=False).notification_type_email = request.POST.getlist('notification_type_email')
            form.save(commit=False).notification_type_phone = request.POST.getlist('notification_type_phone')
            form.save(commit=False).blog_type = request.POST.getlist('types')

            kw = form.cleaned_data['search_keywords']

            if(kw):
                form.save(commit=False).search_keywords = kw.split(", ")

            csv_file = form.cleaned_data['google_a_csv']

            print('======', type(csv_file))

            if(csv_file is not None):
                f = csv_file

                is_google_a_data_good = csv_parser(f)

                if(is_google_a_data_good != None):
                    is_google_a_data_good = True

                    data, total_views, year, months = csv_parser(open(csv_file.path))

                else:
                    is_google_a_data_good = False

                if is_google_a_data_good:
                    avg_views = 0
                    for counter, l in enumerate(data):
                        if counter != 1 or 13:
                            avg_views = avg_views + l[1]

                    avg_views = int(avg_views/12)

                    form.save(commit=False).monthly_views = avg_views

            form.save()

            messages.success(request, "%s has been successfully updated." % (listing.blog_name), extra_tags="blog_listing_update")

        elif form.errors:

            messages.error(request, "There was an error - %s." % (str(form.errors)), extra_tags="blog_listing_update_error")

            return redirect(reverse('blog_listing_update', kwargs={'id': listing.id}))

        return redirect('home')
    return render(request, 'blog_listing_creation.html', context)

@login_required(login_url='login')
@user_is_entry_author
def blogger_listing_delete(request, id=None):
    listing = BlogListingCreationModel.objects.get(id=id)

    messages.success(request, "%s has been successfully deleted." % (listing.blog_name), extra_tags="blog_listing_update")

    context = {
        'listing':listing
    }
    listing.delete()

    return redirect('dashboard')
