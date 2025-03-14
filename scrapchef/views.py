from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def homepage(request):
    # Homepage
    return render(request, 'index.html')

# Login & Signup (Same `auth.html` template)
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                auth_login(request, user)
                return redirect(reverse('scrapchef:homepage'))
            else:
                return HttpResponse("Your ScrapChef account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'auth.html', {'mode': 'login'})

# signup (Uses `auth.html` same as login)
def signup(request):
    return render(request, 'auth.html', {'mode': 'signup'})

# dashboard
def dashboard(request):
    return render(request, 'dashboard.html')

# feed
def feed(request):
    return render(request, 'feed.html')

# privacy policy page (must make this page)
def privacy(request):
    # add stuff here
    return render(request, 'privacy.html')

# saved posts page (must make a page)
@login_required
def saved(request):
    # add stuff here
    return render(request, 'saved.html')

# upload post (Modal inside Dashboard) (need to make the pop up)
@login_required
def post(request):
    return render(request, 'dashboard.html')

# edit post (Modal inside Dashboard) (make page)
@login_required
def editpost(request):
    return render(request, 'dashboard.html')

# trending feed  (make page)
def trending(request):
    return render(request, 'feed.html')

# bestmeals feed  (make page)
def bestmeals(request):
    return render(request, 'feed.html')

# worst Meals feed (make page)
def worstmeals(request):
    # add stuff here
    return render(request, 'feed.html')

# recent meals by date (make page)
def recent(request):
    return render(request, 'feed.html')

# rate a meal (Pop-up inside Feed) (MAKE PAGEEE)
@login_required
def rating(request):
    return render(request, 'feed.html')

# do we have an about page?
def about(request):
    return render(request, 'about.html')

# logout (Redirects to Homepage)
@login_required
def signout(request):
    logout(request)
    return redirect(reverse('scrapchef:homepage'))
