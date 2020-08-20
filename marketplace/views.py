import simplejson as json
from python_stuff.converter import string_to_list, list_to_string #self made python file

from django.shortcuts import render, redirect
from creator_listings.models import BlogListingCreationModel
from sponsor_listings.models import SponsorListingCreationModel
from users.models import UserWatchDashboardModel
from .forms import UserWatchDashboardForm



def creator_marketplace(request):
    creator_listings = BlogListingCreationModel.objects.all()

    context = {
        'creator_listings': creator_listings
    }

    return render(request, 'creator_marketplace.html', context)


def creator_marketplace_listing_view(request, id=None):
    listing = BlogListingCreationModel.objects.get(id=id)
    
    if (request.method == 'POST'):
        form = UserWatchDashboardForm(request.POST or None)
        d_model = UserWatchDashboardModel

        '2, 23, 5'
        ['2', '23', '5']


        '''ppl = Model.objects.all()
        print('----------', ppl, '--------type------', type(ppl))'''

        '''jsonDec = json.decoder.JSONDecoder()
        mylist = jsonDec.decode(myModel.watched_creator) #list of currently watching creators

        mylist.append(listing.id)

        myModel.watched_creator = json.dumps(mylist)'''

        watching = d_model.objects.get(user=request.user.id).watched_creator #string value of all
        watching_list = string_to_list(watching)


        #print('-------------------', watching, '--------type------', type(watching))

        if (form.is_valid()):
            print('--------- form valid ---------')
            specific_user_dashboard_qset = d_model.objects.filter(user=request.user.id)
            data = form.cleaned_data.get("watched_creator") #string value of the button (whether it's watched or watch)
            
            if specific_user_dashboard_qset.exists(): #if this user has ever made watched a listing before
                print('--------- user is good ---------')
                if (listing.id in watching_list):
                    if (data == "Watch"):
                        print('--------- listing has been added to watched ---------')
                        watching_list.append(str(listing.id))
                        watching_string = list_to_string(watching_list)
                        specific_user_dashboard_qset.update(watched_creator=watching_string)
                    elif (data == "Watched"):
                        print('--------- listing has been removed from watched ---------')
                        watching_list.remove(str(listing.id))
                        watching_string = list_to_string(watching_list)
                        specific_user_dashboard_qset.update(watched_creator=watching_string)
            
                elif (listing.id not in watching_list):
                    print('--------- listing not in watched but has been added ---------')
                    watching_list.append(str(listing.id))
                    watching_string = list_to_string(watching_list)
                    specific_user_dashboard_qset.update(watched_creator=watching_string)
            
            else:
                form.save()


            
            #form.save(commit=False).user = request.user.username
            #form.save()

    context = {
        'listing': listing,
        
    }

    return render(request, 'creator_marketplace_listing_view.html', context)


def sponsor_marketplace(request):
    sponsor_listings = SponsorListingCreationModel.objects.all()

    context = {
        'sponsor_listings': sponsor_listings
    }

    return render(request, 'sponsor_marketplace.html', context)



def sponsor_marketplace_listing_view(request, id=None):
    listing = SponsorListingCreationModel.objects.get(id=id)

    context = {
        'listing': listing
    }

    return render(request, 'sponsor_marketplace_listing_view.html', context)