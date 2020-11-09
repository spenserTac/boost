from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .decorators import user_is_entry_author

from .models import BlogListingCreationModel
from users.models import Profile
from .forms import BlogListingCreationForm

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

        'Initial',
        'Accepted',
        'Escrow',
        'Completed'

    ]

    context = {
        'types': types,
        'notification_types': notification_types,
        'profile': profile,
    }

    print(notification_types)

    if request.method == 'POST':
        form = BlogListingCreationForm(request.POST, request.FILES)


        if form.is_valid():
            form.save(commit=False).creator = request.user
            form.save(commit=False).blog_type = type_query

            form.save(commit=False).notification_type = request.POST.getlist('notification_types')
            form.save(commit=False).blog_type = request.POST.getlist('types')

            kw = form.cleaned_data['search_keywords']
            form.save(commit=False).search_keywords = kw.split(", ")


            form.save()

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


    types = [
        'Review',
        'Informative',
        'Discussion',
        'Tutorial',
        'Other',
    ]

    notification_types = [

        'Initial',
        'Accepted',
        'Escrow',
        'Completed'

    ]


    original_string = listing.search_keywords
    characters_to_remove = "[]'"

    new_string = original_string
    for character in characters_to_remove:
        new_string = new_string.replace(character, "")

    kw = new_string.split()
    search_kw = " ".join(kw)


    context = {
        'listing':listing,
        'types':types,
        'notification_types': notification_types,
        'search_kw': search_kw,
    }

    if request.method == 'POST':
        form = BlogListingCreationForm(request.POST,request.FILES, instance=listing)
        if form.is_valid():
            form.save(commit=False).notification_type = request.POST.getlist('notification_types')
            form.save(commit=False).blog_type = request.POST.getlist('types')

            kw = form.cleaned_data['search_keywords']
            form.save(commit=False).search_keywords = kw.split(", ")

            form.save()

        return redirect('home')
    return render(request, 'blog_listing_creation.html', context)

@login_required(login_url='login')
@user_is_entry_author
def blogger_listing_delete(request, id=None):
    listing = BlogListingCreationModel.objects.get(id=id)
    context = {
        'listing':listing
    }
    listing.delete()

    return redirect('dashboard')
