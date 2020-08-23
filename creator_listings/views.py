from django.shortcuts import render, redirect
from django.contrib import messages
from .models import BlogListingCreationModel
from .forms import BlogListingCreationForm

def blogger_listing_creation(request):
    if request.method == 'POST':
        form = BlogListingCreationForm(request.POST)
        if form.is_valid():
            form.save(commit=False).creator = request.user
            form.save()

        return redirect('home')
    
    '''if (id):
        listing = BlogListingCreationModel.objects.get(id=id)
        context = {
            'listing': listing
        }

        return render(request, 'blog_listing_creation.html', context)'''

    return render(request, 'blog_listing_creation.html')

def blogger_listing_update(request, id=None):
    listing = BlogListingCreationModel.objects.get(id=id)
    context = {
        'listing':listing
    }
    if request.method == 'POST':
        form = BlogListingCreationForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()

        return redirect('home')
    return render(request, 'blog_listing_creation.html', context)

def blogger_listing_delete(request, id=None):
    listing = BlogListingCreationModel.objects.get(id=id)
    context = {
        'listing':listing
    }
    listing.delete()

    return redirect('dashboard')
    



