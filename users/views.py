from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            '''username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            fname = form.cleaned_data.get('fname')
            lname = form.cleaned_data.get('lname')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password, firstname=fname, lastname=lname, email=email)
            login(request, user)'''

        print(form.errors)

        return redirect('home')

    else:
        form = UserCreationForm(request.POST)

        context = {
            'form': form,
        }

        return render(request, 'signup.html', context)



def dashboard(request):
    return render(request, 'dashboard.html')