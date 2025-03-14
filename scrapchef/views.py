from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def homepage(request):
    # add stuff
    return(HttpResponse)

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('scrapchef:homepage'))
            else:
                return HttpResponse("Your ScrapChef account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'scrapchef/login.html')

def dashboard(request):
    # add stuff here
    return HttpResponse()

def feed(request):
    # add stuff here
    return HttpResponse()

def privacy(request):
    # add stuff here
    return HttpResponse()

def saved(request):
    # add stuff here
    return HttpResponse()

def post(request):
    # add stuff here
    return HttpResponse()

def editpost(request):
    # add stuff here
    return HttpResponse()

def trending(request):
    # add stuff here
    return HttpResponse()

def bestmeals(request):
    # add stuff here
    return HttpResponse()

def worstmeals(request):
    # add stuff here
    return HttpResponse()

def recent(request):
    # add stuff here
    return HttpResponse()

def rating(request):
    # add stuff here
    return HttpResponse()

@login_required
def signout(request):
    logout(request)
    return redirect(reverse('scrapchef:homepage'))