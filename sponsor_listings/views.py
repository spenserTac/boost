from django.shortcuts import render, redirect
from django.contrib import messages
from .models import SponsorListingCreationModel
from .forms import SponsorListingCreationForm

def sponsor_listing_creation(request):
    if request.method == 'POST':
        form = SponsorListingCreationForm(request.POST or None)

        if form.is_valid():
            form.save()

            return redirect('home')
        elif (form.is_valid() == False):
            #messages.success(request, ("There was an error: %s" % form.errors))
            
            return redirect('sponsor_listing')  

        #messages.success(request, ("Sponsor Listing Successfully Created!"))
        
        
    else:
        '''all_tasks = BlogListingCreationModel.objects.all()

        context = {
        'all_tasks': all_tasks
         }'''

        return render(request, 'sponsor_listing_creation.html')