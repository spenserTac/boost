from django.shortcuts import render

def blogger_listing_creation(request):
    return render(request, 'blog_listing_creation.html')