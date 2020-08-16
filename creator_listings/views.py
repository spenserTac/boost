from django.shortcuts import render, redirect
from django.contrib import messages
from .models import BlogListingCreationModel
from .forms import BlogListingCreationForm

def blogger_listing_creation(request):
    if request.method == 'POST':
        form = BlogListingCreationForm(request.POST or None)
        if form.is_valid():
            form.save(commit=False).creator = request.user
            form.save()
        print(form.errors)
        return redirect('home')
        
    else:
        '''all_tasks = BlogListingCreationModel.objects.all()

        context = {
        'all_tasks': all_tasks
         }'''

        return render(request, 'blog_listing_creation.html')