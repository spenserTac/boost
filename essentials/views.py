from django.shortcuts import render

def home(request):


    context = {
        "user": request.user

    }

    return render(request, 'home.html', context)

#######

def cookies_policy(request):


    context = {
        "user": request.user

    }

    return render(request, 'cookies_policy.html', context)

######

def disclaimer_policy(request):


    context = {
        "user": request.user

    }

    return render(request, 'disclaimer_policy.html', context)

######

def terms_and_conditions(request):


    context = {
        "user": request.user

    }

    return render(request, 'terms_and_conditions.html', context)


######

def return_policy(request):


    context = {
        "user": request.user

    }

    return render(request, 'return_policy.html', context)


######

def privacy_policy(request):


    context = {
        "user": request.user

    }

    return render(request, 'privacy_policy.html', context)


######

def about_us(request):


    context = {
        "user": request.user

    }

    return render(request, 'about_us.html', context)
