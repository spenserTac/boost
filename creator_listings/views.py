from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import BlogListingCreationModel
from .forms import BlogListingCreationForm

@login_required(login_url='login')
def blogger_listing_creation(request):
    type_query = request.POST.getlist('blog_type')

    types = {
        'Review': 1,
        'Informative': 2,
        'Discussion': 3,
        'Tutorial': 4,
        'Other': 5,
    }

    context = {
        'types': types,
    }

    if request.method == 'POST':
        form = BlogListingCreationForm(request.POST)

        if form.is_valid():
            form.save(commit=False).creator = request.user
            form.save(commit=False).blog_type = type_query
            form.save()

        return redirect('home')

    return render(request, 'blog_listing_creation.html', context)

'''
@login_required(login_url='login')
def blogger_listing_creation2(request):

    if request.method == 'POST':
        form = BlogListingCreationForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect('blog_listing3')

    return render(request, 'blog_listing_creation2.html')

@login_required(login_url='login')
def blogger_listing_creation3(request):
    if request.method == 'POST':
        form = BlogListingCreationForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect('blog_listing4')

    return render(request, 'blog_listing_creation3.html')

@login_required(login_url='login')
def blogger_listing_creation4(request):
    if request.method == 'POST':
        form = BlogListingCreationForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect('blog_listing5')

    return render(request, 'blog_listing_creation4.html')

@login_required(login_url='login')
def blogger_listing_creation5(request):
    if request.method == 'POST':
        form = BlogListingCreationForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect('blog_listing6')

    return render(request, 'blog_listing_creation5.html')

@login_required(login_url='login')
def blogger_listing_creation6(request):
    if request.method == 'POST':
        form = BlogListingCreationForm(request.POST)
        if form.is_valid():
            form.save()

        
        return redirect('home')

    return render(request, 'blog_listing_creation6.html')
'''



@login_required(login_url='login')
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

@login_required(login_url='login')
def blogger_listing_delete(request, id=None):
    listing = BlogListingCreationModel.objects.get(id=id)
    context = {
        'listing':listing
    }
    listing.delete()

    return redirect('dashboard')
    



