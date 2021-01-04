from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.core.mail import send_mail



from .forms import CustomUserCreationForm, EditProfileForm
from .models import (Profile, CreatorOrderModel, SponsorOrderModel, AcceptedCreatorOrderModel, AcceptedSponsorOrderModel,
CompletedOrderModel, Messages)
from metrics.models import *

from .functions.escrow_functions import *
from . decorators import *

from creator_listings.models import BlogListingCreationModel
from sponsor_listings.models import SponsorListingCreationModel
from django.contrib.auth.models import User
from .forms import CreatorOrderForm, SupportTicketForm, FeatureTicketForm, SponsorEditForm, SponsorReviewForm

from twilio.rest import Client

import threading



accountSID = 'AC1af4a638ba64727a7fc59d63836fe78d'
authToken  = '84207d244c6aa2868cfdc5df45df008d'
twilioCli = Client(accountSID, authToken)
myTwilioNumber = '+13253996328' #(325) 399-6328
myCellPhone = '13862995508'





# Function that will mark orders complete
def order_complete():
    threading.Timer(600.0, order_complete).start() # called every minute

    orders = AcceptedCreatorOrderModel.objects.filter(status='escrow')

    for order in orders:
        transaction_id = order.transaction_id

        r = requests.get(
            'https://api.escrow-sandbox.com/2017-09-01/transaction/{transaction_id}'.format(transaction_id=transaction_id),
              auth=('admin@getboostplatform.com', '1879_DPJdrsn584BxSiEfOjPD67W9L7acG7JhYmeP3pwv43qmUk31fZtbXz2FAgss0GRY'),
            )

        status = r.json()['items'][0]['status'].get('accepted')
        print(status)

        #print(r.json()['items'][0]['status'].get('accepted'))


        #c_listing = BlogListingCreationModel.objects.get(id=id)
        c_order = AcceptedCreatorOrderModel.objects.get(id=order.id)

        listing = c_order.creator_listing

        Messages.objects.create(sender=c_order.buyer, reciever=c_order.creator, message="Alright Alright Alright, Order For %s is Finalized." % (c_order.buyers_listing_s.product))
        #messages.success(request, "Order is Successfully Finalized. Congradulations!", extra_tags="sponsor_completed_order")
        Messages.objects.create(sender=c_order.creator, reciever=c_order.buyer, message="Alright Alright Alright, Order For %s is Finalized." % (c_order.creator_listing.blog_name))

        if(listing.notification_type_email is not None):
            if('Sponsor Has Marked Order as Complete' in listing.notification_type_email):
                send_mail(
                    'Alright Alright Alright, Order For %s is Finalized.' % (c_order.buyers_listing_s.product),
                    'Congradulations! %s\'s order is now complete. Check it Out https://getboostplatform.com/account/dashboard/.\n\nThank You For Using Boost!' % (c_order.buyers_listing_s.product),
                    'admin@getboostplatform.com',
                    [str(listing.email)],
                    fail_silently=False,
                )

        if(listing.notification_type_phone is not None):
            if('Sponsor Has Marked Order as Complete' in listing.notification_type_phone):

                try:
                    message = twilioCli.messages.create(
                        body="""

                            --- FROM: Boost ---

        Alright Alright Alright, Order For %s is Finalized. Check it Out https://getboostplatform.com/account/dashboard/.

        Thank You For Using Boost!
        """ % (c_order.buyers_listing_s.product),
                        from_=myTwilioNumber,
                        to=str(listing.number)
                        )
                except:
                    pass

        # Accepted creator order (after creator clicks accept)
        cc_order = CompletedOrderModel(
            buyer=c_order.buyer,
            creator=c_order.creator,
            creator_listing=c_order.creator_listing,
            buyer_listing=c_order.buyer_listing,
            buyers_listing_s=c_order.buyers_listing_s,
            buyers_listing_c=c_order.buyers_listing_c,
            service=c_order.service,
            service_detailed=c_order.service_detailed,
            status=c_order.status,
            who_initiated_order=c_order.who_initiated_order,
             payout=c_order.payout,
            )



        cc_order.save()

        CompleteOrderMetricModel.objects.create(
            order_id=cc_order.id
        )

        c_order.delete()



#order_complete()







# id = User.id
@dashboard_edit_profile_decorator
def edit_profile(request, id=None):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(user=user)


    if(request.method == 'POST'):
        form = EditProfileForm(request.POST, instance=request.user)

        context = {'form': form}

        if(form.is_valid()):
            form.save()

            updated_user = User.objects.get(id=id)
            updated_user.email = request.user.username
            updated_user.save()


            return redirect('user_account')

    else:
        form = EditProfileForm(instance=request.user)

        context = {'form': form}

        return render(request, 'change_username.html', context)


def account(request, id=None):
    user = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=request.user)

    type = profile.type

    personal_c_pending_listings = len(CreatorOrderModel.objects.filter(creator=user))
    personal_s_pending_listings = len(SponsorOrderModel.objects.filter(creator=user))
    personal_caccepted_listings = len(AcceptedCreatorOrderModel.objects.filter(creator=user))
    personal_saccepted_listings = len(AcceptedSponsorOrderModel.objects.filter(creator=user))
    personal_completed = len(CompletedOrderModel.objects.filter(creator=user))

    personal_creator_listings = user.bloglistingcreationmodel_set.all()
    personal_sponsor_listings = user.sponsorlistingcreationmodel_set.all()

    i = 0
    ic = 0
    is_ = 0
    for l in personal_creator_listings:
        i += 1
        ic += 1

    for l in personal_sponsor_listings:
        i += 1
        is_ += 1

    ip = 0
    ia = 0
    ic = 0

    context = {
        'personal_c_listings': personal_creator_listings,
        'personal_s_listings': personal_sponsor_listings,
        'num_of_c_listings': ic,
        'num_of_s_listings': is_,
        'num_of_total_listings': i,
        'num_of_cp_listings': personal_c_pending_listings,
        'num_of_sp_listings': personal_s_pending_listings,
        'num_of_ca_listings': personal_caccepted_listings,
        'num_of_ca_listings': personal_saccepted_listings,
        'num_of_completed_listings': personal_completed,
        'type': type,
    }

    return render(request, 'account.html', context)

def delete_account(request):
    user = User.objects.get(username=request.user.username)
    user.delete()

    return redirect('home')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if(User.objects.filter(username=request.POST.get('username')).exists()):
            messages.error(request, "Username already exists", extra_tags="username_exists")
            return redirect('signup')

        if(request.POST.get('password1') != request.POST.get('password2')):
            messages.error(request, "Passwords Do Not Match", extra_tags="passwords_dont_match")
            return redirect('signup')

        if form.is_valid():

            if(form.cleaned_data.get('password1') == form.cleaned_data.get('password2')):

                user = form.cleaned_data.get('username')

                form.save(commit=False).email = user
                form.save()

                messages.success(request, 'User Created For: ' + user)

                return redirect('login')

        messages.error(request, 'Invalid Input For Password', extra_tags="invalid_password")

        context = {
            'form': form,
        }
        return render(request, 'signup.html', context)

    else:
        form = CustomUserCreationForm(request.POST)
        context = {
            'form': form,
        }
        return render(request, 'signup.html', context)


def support_contact(request):
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        users_email = request.POST.get('email')
        problem = request.POST.get('problem')

        if form.is_valid():
            form.save(commit=False).email = users_email
            form.save(commit=False).problem = problem
            form.save()

            messages.success(request, 'Support Ticket Sent Successfully', extra_tags="succussful_support_ticket")

            '''try:
                message = twilioCli.messages.create(
                    body="""

                    --- FROM: Boost ---

(1) - You Have Been Hacked. Do Not Be Alarmed %s ... Well, On Second Thought, You Should be Alarmed. Boost - https://getboostplatform.com/account/dashboard/.

Thank You For Using Boost!
    """ % ('TESTTTTTTTTT'),
                    from_=myTwilioNumber,
                    to=str(13862995508)
                    )
            except:
                print('Error')
                pass'''

            '''send_mail(

                'Test Message',
                'This is a test message \n\nThank You For Using Boost!',
                '',
                [str(users_email)],
                fail_silently=False,
            )'''

            return redirect('home')

    return render(request, 'support.html')

@login_required(login_url='login')
def feature_add(request):
    if request.method == 'POST':

        form = FeatureTicketForm(request.POST)

        if form.is_valid():

            form.save(commit=False).creator = request.user
            form.save()

            messages.success(request, 'Feature Request Ticket Sent Successfully', extra_tags="succussful_feature_ticket")

            return redirect('home')

    return render(request, 'feature.html')


@login_required(login_url='login')
@dashboard_message_decorator
def delete_message(request, id=None):
    message = Messages.objects.get(id=id)
    message.delete()

    return redirect('dashboard')


@login_required(login_url='login')
def dashboard(request):

    #
    # Basic Info
    #

    user = User.objects.get(username=request.user) # current logged in user
    profile = Profile.objects.get(user=user) # current logged in users Profile

    c_watching = profile.creators_watched.all()
    s_watching = profile.sponsors_watched.all()

    c_watch_len = c_watching.count()
    s_watch_len = s_watching.count()
    total_watch_len = c_watch_len + s_watch_len



    #
    # Orders on users listings
    #

    # The logged in users creator listing orders
    c_orders = CreatorOrderModel.objects.filter(creator=user)
    c_orders_len = c_orders.count()

    # The logged in users sponsor listing orders
    s_orders = SponsorOrderModel.objects.filter(creator=user)
    s_orders_len = s_orders.count()



    #
    # Orders user has made
    #

    # The creator and sponsor ORDERS the logged in user has made
    c_ordered = CreatorOrderModel.objects.filter(buyer=user) # profile.creators_u_ordered.all()
    c_ordered_len = c_ordered.count()
    s_ordered = SponsorOrderModel.objects.filter(buyer=user) # profile.sponsors_u_ordered.all()
    s_ordered_len = s_ordered.count()



    #
    # Accepted Orders
    #

    # The ACCEPTED creator and sponsor ORDERS the logged in user has made
    accepted_c_orders = AcceptedCreatorOrderModel.objects.filter(buyer=user)



    # The orders that the logged in user has accepted whether they initiated or not
    c_accepted_orders = AcceptedCreatorOrderModel.objects.filter(creator=user).exclude(status='escrow')
    c_accepted_orders_len = c_accepted_orders.count()

    c_accepted_orders_s = AcceptedCreatorOrderModel.objects.filter(buyer=user).exclude(status='escrow')
    c_accepted_orders_len_s = c_accepted_orders_s.count()


    #
    # Accepted Escrow Orders
    #


    # The orders that have gone to ESCROW status
    c_accepted_orders_escrow = AcceptedCreatorOrderModel.objects.filter(creator=user, status='escrow')
    c_accepted_orders_escrow_len = c_accepted_orders_escrow.count()

    c_accepted_orders_escrow_next = AcceptedCreatorOrderModel.objects.filter(creator=user, status='escrow', stage='upload_url')

    ###########

    c_accepted_orders_escrow_s = AcceptedCreatorOrderModel.objects.filter(buyer=user, status='escrow')
    c_accepted_orders_escrow_len_s = c_accepted_orders_escrow_s.count()

    c_accepted_orders_escrow_s_next = AcceptedCreatorOrderModel.objects.filter(buyer=user, status='escrow', stage='upload_url')


    s_accepted_orders = AcceptedSponsorOrderModel.objects.filter(creator=user)
    s_accepted_orders_len = s_accepted_orders.count()




    # The COMPLETED creator and sponsor ORDERS the logged in user has made
    completed_c_orders_not_initiated = CompletedOrderModel.objects.filter(creator=user, who_initiated_order='sponsor')
    completed_c_orders_initiated = CompletedOrderModel.objects.filter(creator=user, who_initiated_order='creator')

    completed_s_orders_not_initiated = CompletedOrderModel.objects.filter(buyer=user, who_initiated_order='creator')
    completed_s_orders_initiated = CompletedOrderModel.objects.filter(buyer=user, who_initiated_order='sponsor')





    # The created listings of each type (creator and sponsor), if they created any
    personal_creator_listings = user.bloglistingcreationmodel_set.all()
    p_c_listing_len = personal_creator_listings.count()
    personal_sponsor_listings = user.sponsorlistingcreationmodel_set.all()
    p_s_listing_len = personal_sponsor_listings.count()

    your_messages = Messages.objects.filter(reciever=user)


    context = {

        'your_messages': your_messages,

        'personal_c_listings': personal_creator_listings,
        'personal_s_listings': personal_sponsor_listings,

        's_watching': s_watching,
        'c_watching': c_watching,

        'c_watch_len': c_watch_len,
        's_watch_len': s_watch_len,

        'total_watch_len': total_watch_len,

        's_ordered': s_ordered,
        'c_ordered': c_ordered,

        'c_ordered_len': c_ordered_len,
        's_ordered_len': s_ordered_len,

        's_orders': s_orders,
        's_orders_len': s_orders_len,
        'c_orders': c_orders,
        'c_orders_len': c_orders_len,

        'c_accepted_orders': c_accepted_orders,
        'c_accepted_orders_len': c_accepted_orders_len,

        'c_accepted_orders_escrow': c_accepted_orders_escrow,
        'c_accepted_orders_escrow_len': c_accepted_orders_escrow_len,
        'c_accepted_orders_escrow_s': c_accepted_orders_escrow_s,
        'c_accepted_orders_escrow_len_s': c_accepted_orders_escrow_len_s,

        'c_accepted_orders_escrow_next': c_accepted_orders_escrow_next,
        'c_accepted_orders_escrow_s_next': c_accepted_orders_escrow_s_next,

        'c_accepted_orders_s': c_accepted_orders_s,
        'c_accepted_orders_len_s': c_accepted_orders_len_s,

        's_accepted_orders': s_accepted_orders,
        's_accepted_orders_len': s_accepted_orders_len,

        'accepted_c_orders': accepted_c_orders,

        'completed_c_orders_not_initiated': completed_c_orders_not_initiated,
        'completed_c_orders_initiated': completed_c_orders_initiated,
        'completed_s_orders_not_initiated': completed_s_orders_not_initiated,
        'completed_s_orders_initiated': completed_s_orders_initiated,

        'total_orders_num': (c_orders_len + s_orders_len),
        'total_acc_orders_num': (c_accepted_orders_len + s_accepted_orders_len),

        'p_c_listing_len': p_c_listing_len,
        'p_s_listing_len': p_s_listing_len,

        'total_listings_num': (p_c_listing_len + p_s_listing_len),

        'profile': profile,
    }

    return render(request, 'dashboard.html', context)




@login_required(login_url='login')
def dashboard_type_c(request):

    user = request.user
    profile = Profile.objects.get(user=user)

    profile.type = 'creator'
    profile.save()

    return redirect('dashboard')

@login_required(login_url='login')
def dashboard_type_s(request):

    user = request.user
    profile = Profile.objects.get(user=user)

    profile.type = 'sponsor'
    profile.save()

    return redirect('dashboard')

@dashboard_send_review_decorator
def dashboard_send_review(request, id=None):
    # 1. This is for the creator to send over the content they made to the sponsor
    #    so they can view it and approve it.
    # 2. There'll be form stuff here so the content the creator adds to this url
    #    is saved in the DB, so it can then be displayed to the sponsor in the
    #    "Creators To Review" section in the dashboard.

    listing = AcceptedCreatorOrderModel.objects.get(id=id)
    turn = listing.turn

    if(request.method == 'POST'):

        form = SponsorReviewForm(request.POST, request.FILES)

        if form.is_valid():
            file = form.cleaned_data.get('review_file')
            listing.review_file = file
            listing.turn = 's'
            listing.stage = 'review_content_sent'
            listing.save()

            CreatorSendsContentMetricModel.objects.create(order_id=listing.id)

            messages.success(request, 'You have successfully sent reviewable content', extra_tags="review_content_sent_successful")
            Messages.objects.create(sender=listing.creator, reciever=listing.buyer, message='Hooray! Your Content For %s is Ready For Your Review.' % listing.creator_listing.blog_name)

            if(listing.buyers_listing_s.notification_type_email is not None):
                if('Creator Has Sent Content For Review' in listing.buyers_listing_s.notification_type_email):
                    send_mail(
                        'Hooray! Your Content For %s is Ready For Your Review.' % (listing.buyers_listing_s.product),
                        '%s has sent over some content for your review for listing %s. Check it Out https://getboostplatform.com/account/dashboard/.\n\nThank You For Using Boost!' % (listing.creator_listing.blog_name, listing.buyers_listing_s.product),
                        'admin@getboostplatform.com',
                        [str(listing.buyers_listing_s.email)],
                        fail_silently=False,
                    )
            if(listing.buyers_listing_s.notification_type_phone is not None):
                if('Creator Has Sent Content For Review' in listing.buyers_listing_s.notification_type_phone):

                    try:
                        message = twilioCli.messages.create(
                            body="""

                                --- FROM: Boost ---

            Hooray! Your Content For %s is Ready For Your Review. Check it Out https://getboostplatform.com/account/dashboard/.

            Thank You For Using Boost!
            """ % (listing.buyers_listing_s.product),
                            from_=myTwilioNumber,
                            to=str(listing.buyers_listing_s.number)
                            )
                    except:
                        pass

            return redirect('dashboard')

    content = {
        'listing': listing,
    }


    return render(request, 'send_review.html')

@dashboard_s_acc_decorator
def dashboard_s_acc(request, id=None):
    # 1. Make "sponsor_change" = None in the DB for this specific order.
    # 2. Do logic to put this order back in the "Sponsor Accepted Orders" tab,
    #    and in the tamplate there's logic for displaying the right buttons
    # 3. Add escrow.com script here for the sponsor.
    listing = AcceptedCreatorOrderModel.objects.get(id=id)

    listing.turn = 'c'

    listing.sponsor_approves = True
    listing.status = 'escrow'
    listing.stage = 'just_accepted'

    SponsorInitiatesEscrowMetricModel.objects.create(order_id=listing.id)

    Messages.objects.create(sender=listing.buyer, reciever=listing.creator, message='Congrats! Your Content Has Been Approved By %s. Escrow.com should has emailed you a link to the transaction (you may have to check your spam folder).' % listing.buyers_listing_s.product)

    #escrow_sponsor_pays(creator_email, sponsor_email, amount, creator_listing_name()
    if (listing.who_initiated_order == 'sponsor'):
        escrow_t = escrow_sponsor_pays(listing.creator_listing.email, listing.buyers_listing_s.email, listing.payout, listing.creator_listing.blog_name, listing.buyers_listing_s.product)


        #listing.token = encrypt_token(escrow_t["token"])
        listing.token = escrow_t["token"]
        #listing.transaction_id = encrypt_id(escrow_t["transaction_id"])
        listing.transaction_id = escrow_t["transaction_id"]


        listing.save()

    elif (listing.who_initiated_order == 'creator'):
        escrow_t = escrow_creator_pays(listing.creator_listing.email, listing.buyers_listing_s.email, listing.payout, listing.creator_listing.blog_name, listing.buyers_listing_s.product)


        #listing.token = encrypt_token(escrow_t["token"])
        listing.token = escrow_t["token"]
        #listing.transaction_id = encrypt_id(escrow_t["transaction_id"])
        listing.transaction_id = escrow_t["transaction_id"]


        listing.save()

    messages.success(request, 'Escrow transaction for %s has been successfully created' % listing.buyers_listing_s.product, extra_tags="escrow_transaction_sponsor_successful")

    if(listing.creator_listing.notification_type_email is not None):
        if('Sponsor Has Initiated Escrow Process' in listing.creator_listing.notification_type_email):
            send_mail(
                'Congrats! Your Content Has Been Approved By %s.' % (listing.buyers_listing_s.product),
                '%s has started the escrow process for your listing %s. Escrow.com should has sent emailed you with a link to the transaction (you may have to check your spam folder).\n\nThank You For Using Boost!' % (listing.buyers_listing_s.product, listing.creator_listing.blog_name),
                'admin@getboostplatform.com',
                [str(listing.creator_listing.email)],
                fail_silently=False,
            )
    if(listing.creator_listing.notification_type_phone is not None):
        if('Sponsor Has Initiated Escrow Process' in listing.creator_listing.notification_type_phone):

            try:
                message = twilioCli.messages.create(
                    body="""

                        --- FROM: Boost ---

    Congrats! Your Content Has Been Approved By %s. Escrow.com should have emailed you a link to join the transaction (you may have to check your spam folder).

    Thank You For Using Boost!
    """ % (listing.buyers_listing_s.product),
                    from_=myTwilioNumber,
                    to=str(listing.creator_listing.number)
                    )
            except:
                pass


    content = {
        'listing': listing,
    }
    return redirect('https://www.escrow-sandbox.com/pay?token=%s' % (escrow_t["token"]), "_blank")

@dashboard_s_edit_decorator
def dashboard_s_edit(request, id=None):
    # 1. There'll be form stuff here, and all this funciton is designed for is
    #    to add whatever edits the sponsor wants to make to the creators content

    listing = AcceptedCreatorOrderModel.objects.get(id=id)

    turn = listing.turn

    if(request.method == 'POST'):
        form = SponsorEditForm(request.POST)

        if form.is_valid():
            edit = form.cleaned_data.get('edits')
            listing.edits = edit
            listing.turn = 'c'
            listing.stage = 'sponsor_edits_sent'
            listing.save()

            SponsorSendsEditsMetricModel.objects.create(order_id=listing.id)

            messages.success(request, '%s' % listing.creator_listing.blog_name, extra_tags="edits_sponsor_successful")
            Messages.objects.create(sender=listing.buyer, reciever=listing.creator, message="Alert! Alert! %s Has Requested Some Edits For Your Listing %s" % (listing.buyers_listing_s, listing.creator_listing.blog_name))

            if(listing.creator_listing.notification_type_email is not None):
                if('Sponsor Has Sent Edits For Accepted Order' in listing.creator_listing.notification_type_email):
                    send_mail(
                        'Alert! Alert! %s Has Requested Some Edits For Your Listing %s' % (listing.buyers_listing_s.product, listing.creator_listing.blog_name),
                        '%s has requested some edits for your content for listing %s. Check it Out https://getboostplatform.com/account/dashboard/.\n\nThank You For Using Boost!' % (listing.buyers_listing_s.product, listing.creator_listing.blog_name),
                        'admin@getboostplatform.com',
                        [str(listing.creator_listing.email)],
                        fail_silently=False,
                    )
            if(listing.creator_listing.notification_type_phone is not None):
                if('Sponsor Has Sent Edits For Accepted Order' in listing.creator_listing.notification_type_phone):
                    try:
                        message = twilioCli.messages.create(
                            body="""

                                --- FROM: Boost ---

            Alert! Alert! %s Has Requested Some Edits For Your Listing %s. Check it Out https://getboostplatform.com/account/dashboard/.

            Thank You For Using Boost!
            """ % (listing.buyers_listing_s.product, listing.creator_listing.blog_name),
                            from_=myTwilioNumber,
                            to=str(listing.creator_listing.number)
                            )
                    except:
                        pass

            return redirect('dashboard')

    context = {
        'listing': listing,
    }

    return render(request, 's_edit.html', context)

# This is the function that runs when the creator is ready to uplaod url so the sponsor will be able to see
@dashboard_c_next_step_decorator
def dashboard_c_next_step(request, id=None):
    escrow_order = AcceptedCreatorOrderModel.objects.get(id=id)

    #token = cipher_token(escrow_order.token)
    #t_id = cipher_id(escrow_order.transaction_id)



    if(request.method == 'POST'):

        cont_url = request.POST.get("content_url")
        escrow_order.content_url = cont_url
        escrow_order.turn = 's'
        escrow_order.stage = 'upload_url'

        escrow_order.save()

        CreatorSendsUrlMetricModel.objects.create(order_id=escrow_order.id)

        messages.success(request, 'URL successfully sent to sponsor.', extra_tags="escrow_transaction_url_send_successful")
        Messages.objects.create(sender=escrow_order.creator, reciever=escrow_order.buyer, message='It\'s Go Time! %s Has Uploaded Your Content. The URL: %s' % (escrow_order.creator_listing.blog_name, escrow_order.content_url))

        if(escrow_order.buyers_listing_s.notification_type_email is not None):
            if('Creator Has Sent Content URL' in escrow_order.buyers_listing_s.notification_type_email):
                send_mail(
                    'It\'s Go Time! %s Has Uploaded Your Content. The URL is Available.' % (escrow_order.creator_listing.blog_name),
                    'Check it out here: %s. Go To Your Dashboard To Check It Out https://getboostplatform.com/account/dashboard/.\n\nThank You For Using Boost!' % (escrow_order.content_url),
                    'admin@getboostplatform.com',
                    [str(escrow_order.buyers_listing_s.email)],
                    fail_silently=False,
                )
        if(escrow_order.buyers_listing_s.notification_type_phone is not None):
            if('Creator Has Sent Content URL' in escrow_order.buyers_listing_s.notification_type_phone):
                try:
                    message = twilioCli.messages.create(
                        body="""

                            --- FROM: Boost ---

        It\'s Go Time! %s Has Uploaded Your Content. The URL: %s. Go To Your Dashboard To Check It Out https://getboostplatform.com/account/dashboard/.

        Thank You For Using Boost!
        """ % (escrow_order.creator_listing.blog_name, escrow_order.content_url),
                        from_=myTwilioNumber,
                        to=str(escrow_order.buyers_listing_s.number)
                        )
                except:
                    pass

        return redirect('dashboard')

    return render(request, 'creator_upload_url.html')


# This function is run when the sponsor cant find the url that the creator proveded
    # and the creator is just presented with the option to resend the url.
@dashboard_s_cant_find_url_decorator
def dashboard_s_cant_find_url(request, id=None):
    escrow_order = AcceptedCreatorOrderModel.objects.get(id=id)

    escrow_order.turn = 'c'

    escrow_order.stage = 'send_url_again'

    escrow_order.save()

    SponsorCantFindUrlMetricModel.objects.create(order_id=escrow_order.id)

    messages.success(request, 'Creator has been successfully notified.', extra_tags="escrow_transaction_url_send_c_notification")
    Messages.objects.create(sender=escrow_order.buyer, reciever=escrow_order.creator, message='Oops! There\'s a Problem With The URL Sent To %s. Please Resend a Valid URL.' % (escrow_order.buyers_listing_s.product))

    if(escrow_order.creator_listing.notification_type_email is not None):
        if('Sponsor Claims Content URL is Invalid' in escrow_order.creator_listing.notification_type_email):
            print('email sent')
            send_mail(
                'Oops! There\'s a Problem With The URL Sent To %s' % (escrow_order.buyers_listing_s.product),
                'Please resend valid URL to %s. Go To Your Dashboard To Resend The URL https://getboostplatform.com/account/dashboard/.\n\nThank You For Using Boost!' % (escrow_order.buyers_listing_s.product),
                'admin@getboostplatform.com',
                [str(escrow_order.creator_listing.email)],
                fail_silently=False,
            )
    if(escrow_order.creator_listing.notification_type_phone is not None):
        if('Sponsor Claims Content URL is Invalid' in escrow_order.creator_listing.notification_type_phone):
            try:
                message = twilioCli.messages.create(
                    body="""

                        --- FROM: Boost ---

    Oops! There\'s a Problem With The URL Sent To %s. Please Resend Valid URL. Go To Your Dashboard To Resend The URL https://getboostplatform.com/account/dashboard/.

    Thank You For Using Boost!
    """ % (escrow_order.buyers_listing_s.product),
                    from_=myTwilioNumber,
                    to=str(escrow_order.creator_listing.number)
                    )
            except:
                pass

    return redirect('dashboard')

#
# Watch and unwatch feature on dashboard
#

def dashboard_unwatch_c(request, id=None):
    users_profile = Profile.objects.get(user=request.user)
    listing = users_profile.creators_watched.get(id=id)
    users_profile.creators_watched.remove(listing)

    return redirect('dashboard')

def dashboard_unwatch_s(request, id=None):
    users_profile = Profile.objects.get(user=request.user)
    listing = users_profile.sponsors_watched.get(id=id)
    users_profile.sponsors_watched.remove(listing)



    return redirect('dashboard')

#
# Unordering creators and sponsors
#

# When a sponsor unorders a creator -> Alert creator that it's been unordered
def dashboard_unorder_c(request, id=None):
    users_profile = Profile.objects.get(user=request.user)
    listing = users_profile.creators_u_ordered.get(id=id)
    users_profile.creators_u_ordered.remove(listing)

    creator_order = CreatorOrderModel.objects.get(buyer=request.user, creator_listing=listing)

    Messages.objects.create(sender=creator_order.buyers_listing_s.creator, reciever=creator_order.creator_listing.creator,
        message='%s Has Canceled Their Order' % (creator_order.buyers_listing_s.product))

    messages.success(request, 'You\'ve Successfully Canceled Your Order.', extra_tags="unorder_s_for_c_successful") # Message For creator

    if(creator_order.creator_listing.notification_type_email is not None):
        if('Listing is Unordered' in creator_order.creator_listing.notification_type_email):
            send_mail(
                '%s Has Canceled Their Order' % (creator_order.buyers_listing_s.product),
                '%s has changed their mind, and canceled their order. Check it Out https://getboostplatform.com/account/dashboard/.\n\nThank You For Using Boost!' % (creator_order.buyers_listing_s.product),
                'admin@getboostplatform.com',
                [str(creator_order.creator_listing.email)],
                fail_silently=False,
            )
    if(creator_order.creator_listing.notification_type_phone is not None):
        if('Listing is Unordered' in creator_order.creator_listing.notification_type_phone):

            try:
                message = twilioCli.messages.create(
                    body="""

                        --- FROM: Boost ---

    %s Has Canceled Their Order. Check it Out https://getboostplatform.com/account/dashboard/.

    Thank You For Using Boost!
    """ % (creator_order.buyers_listing_s.product),
                    from_=myTwilioNumber,
                    to=str(creator_order.creator_listing.number)
                    )
            except:
                pass

    creator_order.delete()

    return redirect('dashboard')


# This view has been discontinued. It doesn't make any sense to unorder a creator after you or they accepted (both parties already agreed).
@dashboard_user_is_buyer
def dashbord_unorder_accepted_c(request, id=None):
    order = AcceptedCreatorOrderModel.objects.get(id=id)

    messages.success(request, '%s' % order.creator_listing.blog_name, extra_tags="unorder_acc_creator_successful")

    order.delete()

    return redirect('dashboard')

def dashboard_unorder_s(request, id=None):
    users_profile = Profile.objects.get(user=request.user)
    listing = users_profile.sponsors_u_ordered.get(id=id)
    users_profile.sponsors_u_ordered.remove(listing)

    sponsor_order = SponsorOrderModel.objects.get(buyer=request.user, sponsor_listing=listing)

    listing = sponsor_order

    Messages.objects.create(sender=sponsor_order.buyers_listing_c.creator, reciever=sponsor_order.sponsor_listing.creator,
        message='%s Has Canceled Their Order' % (sponsor_order.buyers_listing_c.blog_name))

    messages.success(request, 'You\'ve Successfully Canceled Your Order.', extra_tags="unorder_creator_for_s_successful")

    if(listing.sponsor_listing.notification_type_email is not None):
        if('Listing is Unordered' in listing.sponsor_listing.notification_type_email):
            print('sent 1')
            send_mail(
                '%s Has Canceled Their Order' % (listing.buyers_listing_c.blog_name),
                '%s has changed their mind, and canceled their order. Check it Out https://getboostplatform.com/account/dashboard/.\n\nThank You For Using Boost!' % (listing.buyers_listing_c.blog_name),
                'admin@getboostplatform.com',
                [str(listing.sponsor_listing.email)],
                fail_silently=False,
            )
    if(listing.sponsor_listing.notification_type_phone is not None):
        if('Listing is Unordered' in listing.sponsor_listing.notification_type_phone):
            try:
                print('sent 2')
                message = twilioCli.messages.create(
                    body="""

                        --- FROM: Boost ---

    %s Has Canceled Their Order. Check it Out https://getboostplatform.com/account/dashboard/.

    Thank You For Using Boost!
    """ % (listing.creator_listing.blog_name),
                    from_=myTwilioNumber,
                    to=str(listing.sponsor_listing.number)
                    )
            except:
                pass

    sponsor_order.delete()


    return redirect('dashboard')

#
# Accept and decline system on dashboard (for orders)
#

#creator accepts sponsor's order
@dashboard_user_is_creator
def dashboard_creator_order_accept(request, id=None):

    try:
        #c_listing = BlogListingCreationModel.objects.get(id=id)
        c_order = CreatorOrderModel.objects.get(id=id)
        c_order.status = 'accepted'

        c_order.save()

        CreatorAccSponsorMetricModel.objects.create(order_id=c_order.id)

        messages.success(request, "Order Has Been Successfully Accepted.", extra_tags="creator_order_accept_success")
        Messages.objects.create(sender=c_order.creator, reciever=c_order.buyer, message="Congrats! Your Order Has Been Accepted By %s." % (c_order.creator_listing.blog_name))

        listing = c_order.buyers_listing_s

        if(listing.notification_type_email is not None):
            if('Order is Accepted by Creator' in listing.notification_type_email):
                print('sent 1')
                send_mail(
                    'Congrats! Your Order Has Been Accepted By %s' % (c_order.creator_listing.blog_name),
                    '%s has accepted your order for listing %s. Check it Out https://getboostplatform.com/account/dashboard/.\n\nThank You For Using Boost!' % (c_order.creator_listing.blog_name, listing.product),
                    'admin@getboostplatform.com',
                    [str(listing.email)],
                    fail_silently=False,
                )
        if(listing.notification_type_phone is not None):
            if('Order is Accepted by Creator' in listing.notification_type_phone):

                try:
                    print('sent 2')
                    message = twilioCli.messages.create(
                        body="""

                            --- FROM: Boost ---

        Congrats! Your Order Has Been Accepted By %s. Check it Out https://getboostplatform.com/account/dashboard/.

        Thank You For Using Boost!
        """ % (c_order.creator_listing.blog_name),
                        from_=myTwilioNumber,
                        to=str(listing.number)
                        )
                except:
                    pass

        # Accepted creator order (after creator clicks accept)
        ac_order = AcceptedCreatorOrderModel(
            buyer=c_order.buyer,
            creator=c_order.creator,
            creator_listing=c_order.creator_listing,
            buyer_listing=c_order.buyer_listing,
            buyers_listing_s=c_order.buyers_listing_s,
            buyers_listing_c=c_order.buyers_listing_c,
            service=c_order.service,
            service_detailed=c_order.service_detailed,
            status=c_order.status,
            who_initiated_order='sponsor',
            payout=c_order.payout,
            s_content_file=c_order.s_content_file,
            stage='initial_stage'
            )

        ac_order.save()
        c_order.delete()

    except CreatorOrderModel.DoesNotExist:
        #s_listing = SponsorListingCreationModel.objects.get(id=id)
        s_order = SponsorOrderModel.objects.get(id=id)
        s_order.status = 'accepted'

        s_order.save()

        # Accepted creator order (after creator clicks accept)
        as_order = AcceptedSponsorOrderModel(
            buyer=s_order.buyer,
            creator=s_order.creator,
            sponsor_listing=s_order.sponsor_listing,
            buyer_listing=s_order.buyer_listing,
            buyers_listing_s=s_order.buyers_listing_s,
            buyers_listing_c=s_order.buyers_listing_c,
            services_creator_is_willing_to_provide=s_order.services_creator_is_willing_to_provide,
            services_creator_is_willing_to_provide_detailed=s_order.services_creator_is_willing_to_provide_detailed,
            status=s_order.status
            #stage='initial_stage'

        )

        as_order.save()
        s_order.delete()


    return redirect('dashboard')

# When a creator declines a sponsor | sender = creator, reciever = sponsor
@dashboard_user_is_creator
def dashboard_creator_order_decline(request, id=None):
    try:
        c_order = CreatorOrderModel.objects.get(id=id)
        c_order.status = 'declined'

        if(request.method == 'POST'):
            message = request.POST.get("decline_explanation")

            Messages.objects.create(sender=c_order.creator, reciever=c_order.buyer, message="Uh Oh. %s Declined Your Order. Explanation: %s" % (c_order.creator_listing.blog_name, message))
            messages.success(request, "%s has been successfully declined." % (c_order.buyers_listing_s.product), extra_tags="creator_declines_sponsor")

            listing = c_order

            if(listing.buyers_listing_s.notification_type_email is not None):
                if('Order is Declined by Creator' in listing.buyers_listing_s.notification_type_email):
                    send_mail(
                        'Uh Oh. %s Declined Your Order.' % (listing.creator_listing.blog_name),
                        '%s has declined the order because %s. Check it Out https://getboostplatform.com/account/dashboard/.\n\nThank You For Using Boost!' % (listing.creator_listing.blog_name, message),
                        'admin@getboostplatform.com',
                        [str(listing.buyers_listing_s.email)],
                        fail_silently=False,
                    )

            if(listing.buyers_listing_s.notification_type_phone is not None):
                if('Order is Declined by Creator' in listing.buyers_listing_s.notification_type_phone):
                    try:
                        message = twilioCli.messages.create(
                            body="""

                                --- FROM: Boost ---

            Uh Oh. %s Declined Your Order. Explanation: %s Check it Out https://getboostplatform.com/account/dashboard/.

            Thank You For Using Boost!
            """ % (listing.creator_listing.blog_name, message),
                            from_=myTwilioNumber,
                            to=str(listing.buyers_listing_s.number)
                            )
                    except:
                        pass

            c_order.delete()

            return redirect('dashboard')

        return render(request, 'creator_unorder_message.html')

    except CreatorOrderModel.DoesNotExist:
        s_order = SponsorOrderModel.objects.get(id=id)
        s_order.status = 'declined'



        s_order.delete()

    return redirect('dashboard')


# When a sponsor accepts a creator | sender = sponsor, reciever = creator
@dashboard_user_is_buyer
def dashboard_sponsor_order_accept(request, id=None):

    order = SponsorOrderModel.objects.get(id=id)

    creator_listing = BlogListingCreationModel.objects.get(id=order.buyers_listing_c.id)
    profile = Profile.objects.get(user=request.user)

    profile.creators_u_ordered.add(creator_listing)

    buyer = request.user
    buyer_profile = Profile.objects.get(user=buyer)
    buyers_sponsor_listings = buyer.sponsorlistingcreationmodel_set.all()
    buyers_creator_listings = buyer.bloglistingcreationmodel_set.all()

    creator = creator_listing.creator


    if (request.method == 'POST'):
        # add instance field for updating -> , instance=prev_c_order
        form = CreatorOrderForm(request.POST or None, request.FILES)

        if (form.is_valid()):
            SponsorAccCreatorMetricModel.objects.create(order_id=order.id)

            obj = form.save(commit=False)
            obj.payout = form.cleaned_data['payout']

            order.status = 'accepted'
            obj.s_content_file = form.cleaned_data['s_content_file']

            messages.success(request, "%s has been successfully accepted." % (order.buyers_listing_c.blog_name), extra_tags="sponsor_acceptes_creator")
            Messages.objects.create(sender=order.creator, reciever=order.buyer, message="Congrats! Your Order Has Been Accepted By %s" % (order.sponsor_listing.product))

            listing = creator_listing

            if( listing.notification_type_email is not None):
                if('Order is Accepted by Sponsor' in listing.notification_type_email):
                    send_mail(
                        'Congrats! Your Order Has Been Accepted By %s' % (order.sponsor_listing.product),
                        '%s has accepted your order for listing %s. Check it Out https://getboostplatform.com/account/dashboard/.\n\nThank You For Using Boost!' % (order.sponsor_listing.product, order.buyers_listing_c.blog_name),
                        'admin@getboostplatform.com',
                        [str(listing.email)],
                        fail_silently=False,
                    )

            if( listing.notification_type_phone is not None):
                if('Order is Accepted by Sponsor' in listing.notification_type_phone):

                    try:
                        message = twilioCli.messages.create(
                            body="""

                                --- FROM: Boost ---

            Congrats! Your Order Has Been Accepted By %s. Check it Out https://getboostplatform.com/account/dashboard/.

            Thank You For Using Boost!
            """ % (order.sponsor_listing.product),
                            from_=myTwilioNumber,
                            to=str(listing.number)
                            )
                    except:
                        pass

            order.save()

            # Accepted creator order (after creator clicks accept)



            ac_order = AcceptedCreatorOrderModel(
                buyer=request.user,
                creator=creator_listing.creator,
                creator_listing=creator_listing,
                buyer_listing=order.sponsor_listing,
                buyers_listing_s=order.sponsor_listing,

                service=obj.service,
                service_detailed=obj.service_detailed,

                status='accepted',
                who_initiated_order = 'creator',
                payout = obj.payout,
                s_content_file = obj.s_content_file,
                stage='initial_stage'
                )

            ac_order.save()
            order.delete()

            #obj.save()

            return redirect('dashboard')


    return render(request, 'acceptedcreator.html')

# When a sponsor declines a creator | sender = sponsor, reciever = creator
@dashboard_user_is_buyer
def dashboard_sponsor_order_decline(request, id=None):

    try:
        #c_listing = BlogListingCreationModel.objects.get(id=id)
        c_order = CreatorOrderModel.objects.get(id=id)
        c_order.status = 'declined'

        c_order.delete()

    except CreatorOrderModel.DoesNotExist:
        #s_listing = SponsorListingCreationModel.objects.get(id=id)
        s_order = SponsorOrderModel.objects.get(id=id)
        s_order.status = 'declined'

        if(request.method == 'POST'):
            message = request.POST.get("decline_explanation")

            Messages.objects.create(sender=s_order.creator, reciever=s_order.buyer, message="Uh Oh. %s Declined Your Order. Explanation: %s" % (s_order.sponsor_listing.product, message))
            messages.success(request, "%s has been successfully declined." % (s_order.buyers_listing_c.blog_name), extra_tags="sponsor_declined_creator")

            listing = s_order.buyers_listing_c

            if(listing.notification_type_email is not None):
                if('Order is Declined by Sponsor' in listing.notification_type_email):
                    send_mail(
                        'Uh Oh. %s Declined Your Order.' % (s_order.sponsor_listing.product),
                        '%s has declined the order because %s. Check it Out https://getboostplatform.com/account/dashboard/.\n\nThank You For Using Boost!' % (s_order.sponsor_listing.product, message),
                        'admin@getboostplatform.com',
                        [str(listing.email)],
                        fail_silently=False,
                    )

            if(listing.notification_type_phone is not None):
                if('Order is Declined by Sponsor' in listing.notification_type_phone):

                    try:
                        message = twilioCli.messages.create(
                            body="""

                                --- FROM: Boost ---

            Uh Oh. %s decline your order because %s. Check it Out https://getboostplatform.com/account/dashboard/.

            Thank You For Using Boost!
            """ % (s_order.sponsor_listing.product, message),
                            from_=myTwilioNumber,
                            to=str(listing.number)
                            )
                    except:
                        pass

            s_order.delete()

            return redirect('dashboard')

        return render(request, 'sponsor_unorder_message.html')

    return redirect('dashboard')

'''

@dashboard_sponsor_complete_order
def dashboard_creator_order_complete(request, id=None):
    order = AcceptedCreatorOrderModel.objects.get(id=id)
    order.status = 'complete'
    order.save()


    try:
        #c_listing = BlogListingCreationModel.objects.get(id=id)
        c_order = AcceptedCreatorOrderModel.objects.get(id=id)
        c_order.status = 'complete'

        c_order.save()

        listing = c_order.creator_listing

        Messages.objects.create(sender=c_order.buyer, reciever=c_order.creator, message="Alright Alright Alright, Order For %s is Finalized." % (c_order.buyers_listing_s.product))
        messages.success(request, "Order is Successfully Finalized. Congradulations!", extra_tags="sponsor_completed_order")

        if(listing.notification_type_email is not None):
            if('Sponsor Has Marked Order as Complete' in listing.notification_type_email):
                send_mail(
                    'Alright Alright Alright, Order For %s is Finalized.' % (c_order.buyers_listing_s.product),
                    'Congradulations! %s\'s order is now complete. Check it Out https://getboostplatform.com/account/dashboard/.\n\nThank You For Using Boost!' % (c_order.buyers_listing_s.product),
                    'admin@getboostplatform.com',
                    [str(listing.email)],
                    fail_silently=False,
                )

        if(listing.notification_type_phone is not None):
            if('Sponsor Has Marked Order as Complete' in listing.notification_type_phone):

                try:
                    message = twilioCli.messages.create(
                        body="""

                            --- FROM: Boost ---

        Alright Alright Alright, Order For %s is Finalized. Check it Out https://getboostplatform.com/account/dashboard/.

        Thank You For Using Boost!
        """ % (c_order.buyers_listing_s.product),
                        from_=myTwilioNumber,
                        to=str(listing.number)
                        )
                except:
                    pass

        # Accepted creator order (after creator clicks accept)
        cc_order = CompletedOrderModel(
            buyer=c_order.buyer,
            creator=c_order.creator,
            creator_listing=c_order.creator_listing,
            buyer_listing=c_order.buyer_listing,
            buyers_listing_s=c_order.buyers_listing_s,
            buyers_listing_c=c_order.buyers_listing_c,
            service=c_order.service,
            service_detailed=c_order.service_detailed,
            status=c_order.status,
            who_initiated_order=c_order.who_initiated_order,
            payout=c_order.payout,
            )

        cc_order.save()
        c_order.delete()

    #This should probably be removed and has no functions
    except CreatorOrderModel.DoesNotExist:
        #s_listing = SponsorListingCreationModel.objects.get(id=id)
        s_order = SponsorOrderModel.objects.get(id=id)
        s_order.status = 'complete'

        s_order.save()

        # Accepted creator order (after creator clicks accept)
        as_order = AcceptedSponsorOrderModel(
            buyer=s_order.buyer,
            creator=s_order.creator,
            sponsor_listing=s_order.sponsor_listing,
            buyer_listing=s_order.buyer_listing,
            buyers_listing_s=s_order.buyers_listing_s,
            buyers_listing_c=s_order.buyers_listing_c,
            services_creator_is_willing_to_provide=s_order.services_creator_is_willing_to_provide,
            services_creator_is_willing_to_provide_detailed=s_order.services_creator_is_willing_to_provide_detailed,
            status=s_order.status

        )

        as_order.save()
        s_order.delete()

    return redirect('dashboard')

'''
# This view is no longer in use, and should probably be removed
'''def dashboard_sponsor_order_complete(request, id=None):

    order = AcceptedSponsorOrderModel.objects.get(id=id)
    order.status = 'complete'
    order.save()

    return redirect('dashboard')'''

@dashboard_withdraw_decorator
def dashboard_withdraw_order(request, id=None):
    order = AcceptedCreatorOrderModel.objects.get(id=id)

    if(request.method == 'POST'):
        CreatorWithdrawsMetricModel.objects.create(order_id=order.id)

        message = request.POST.get("withdraw_explanation")

        messages.success(request, "You've Successfully Withdrawn From %s\'s Order." % (order.buyers_listing_s.product), extra_tags="creator_withdraw")
        Messages.objects.create(sender=order.creator, reciever=order.buyer, message="Somthing Has Gone Wrong. %s Has Withdrawn From The Order. Reason: %s" % (order.creator_listing.blog_name, message))

        listing = order.buyers_listing_s



        if(listing.notification_type_email is not None):
            if('Creator Has Withdrawn From Accepted Order' in listing.notification_type_email):
                send_mail(
                    'Somthing Has Gone Wrong. %s Has Withdrawn From The Order.' % (listing.product),
                    'Here\'s why: %s. Check it Out https://getboostplatform.com/account/dashboard/.\n\nThank You For Using Boost!' % (message),
                    'admin@getboostplatform.com',
                    [str(listing.email)],
                    fail_silently=False,
                )
        if(listing.notification_type_phone is not None):
            if('Creator Has Withdrawn From Accepted Order' in listing.notification_type_phone):
                try:
                    message = twilioCli.messages.create(
                        body="""

                            --- FROM: Boost ---

        Somthing Has Gone Wrong. %s Has Withdrawn From The Order. Reason: %s Check it Out https://getboostplatform.com/account/dashboard/.

        Thank You For Using Boost!
        """ % (listing.product, message),
                        from_=myTwilioNumber,
                        to=str(listing.number)
                        )
                except:
                    pass

        order.delete()

        return redirect('dashboard')
    return render(request, 'creator_withdraw_message.html')
