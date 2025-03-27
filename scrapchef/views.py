from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from scrapchef.models import Post, Review
from django.contrib.auth.models import User
from .models import UserProfile
from django.db import IntegrityError
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.messages import get_messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from scrapchef.models import SavedPost
from scrapchef.forms import MakePostForm


def homepage(request):
    return render(request, 'scrapchef/homepage.html')


def privacy_security(request):
    return render(request, 'scrapchef/privacy_security.html')

@login_required
def dashboard(request):
    user = request.user
    profile = UserProfile.objects.get(User=user)
    posts = Post.objects.filter(User=user).order_by('-Date')
    form = MakePostForm()

    for post in posts:
        post.is_url = post.Media.startswith("http")

    return render(request, 'scrapchef/dashboard.html', {
        'user': user,
        'profile': profile,
        'posts': posts,
        'form': form,
    })


@login_required
def upload_post(request):
    
    if request.method == 'POST':

        url = request.POST.get('url')
        media = request.FILES.get('media')
        caption = request.POST.get('caption')

        if not url:
            if not caption or not media:
                messages.error(request, "Missing caption or media.")
                return redirect('scrapchef:dashboard')

            post = Post.objects.create(
                User=request.user,
                Caption=caption,
                Media=media,
                Image=media,
            )
        else:
            if not caption:
                messages.error(request, "Missing caption or media.")
                return redirect('scrapchef:dashboard')
            
            code = str(url).split("/")[-1]
            
            post = Post.objects.create(
                User=request.user,
                Caption=caption,
                Media="https://www.youtube.com/embed/" + code,
            )

        return redirect('scrapchef:dashboard')  # ← REDIRECT to dashboard instead of JSON

    return redirect('scrapchef:dashboard')

def feed(request):
    post_list = Post.objects.order_by('Date')
    avg_ratings = []

    # Get the saved posts for the current user
    if request.user.is_authenticated:
        saved_post_ids = SavedPost.objects.filter(user=request.user).values_list('post_id', flat=True)
    else:
        saved_post_ids = []

    for post in post_list:
        avg_ratings.append(getPostAvgRatings(post))

    # Add a new attribute to check if media is a URL
    for post in post_list:
        post.is_url = post.Media.startswith("http")

    context_dict = {
        'zip_post_ratings': zip(post_list, avg_ratings),
        'saved_post_ids': saved_post_ids,  # Pass saved post IDs to the template
    }
    
    return render(request, 'scrapchef/feed.html', context=context_dict)


def privacy(request):
    # add stuff here
    return render(request, 'scrapchef/privacy.html')


@login_required
def save_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    saved_post, created = SavedPost.objects.get_or_create(user=request.user, post=post)
    if not created:
        messages.info(request, "This post is already saved.")
    else:
        messages.success(request, "Post saved successfully.")
    return redirect(f'/feed/?success=saved')

@login_required
def unsave_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    saved_post = SavedPost.objects.filter(user=request.user, post=post)
    if saved_post.exists():
        saved_post.delete()
    return redirect(f'/feed/?success=unsaved')
  # Redirect to saved posts page

@login_required
def saved(request):
    saved_posts = SavedPost.objects.filter(user=request.user)
    posts = [saved_post.post for saved_post in saved_posts]
    avg_ratings = []

    for post in posts:
        avg_ratings.append(getPostAvgRatings(post))

    # Add a new attribute to check if media is a URL
    for post in posts:
        post.is_url = post.Media.startswith("http")

    context = {
        'zip_post_ratings': zip(posts, avg_ratings),
    }
    return render(request, 'scrapchef/saved.html', context)



def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        occupation = request.POST.get("occupation", "").strip()
        profile_photo = request.FILES.get("profile_photo", None)

        if not username or not password:
            messages.error(request, "Username and password are required.")
            return redirect("scrapchef:signup_view")

        if not username.isalnum():
            messages.error(request, "Username must contain only letters and numbers.")
            return redirect("scrapchef:signup_view")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("scrapchef:signup_view")

        try:
            user = User.objects.create_user(username=username, password=password)
            user_profile = UserProfile.objects.get(User=user)
            user_profile.Occupation = occupation
            user_profile.Profile_photo = ""
            user_profile.save()
            user.save()

            messages.success(request, "Signup successful! Please log in.")
            return redirect(reverse_lazy("scrapchef:login_view"))

        except IntegrityError:
            messages.error(request, "An error occurred. Please try again.")
            return redirect("scrapchef:signup_view")

    return render(request, "scrapchef/signup.html")


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect(reverse('scrapchef:dashboard'))
        else:
            return HttpResponse("Invalid username or password.")
    
    return render(request, 'scrapchef/login.html')

def post(request):
    # add stuff here
    return render(request, 'scrapchef/post.html')


def editpost(request, post_name_slug):
    # context dict has simply the post that is being edited, or None if it doesn't exist
    context_dict = {}
    try:
        post = Post.objects.get(slug=post_name_slug)
        context_dict['post'] = post
    except Post.DoesNotExist:
        context_dict['post'] = None

    return render(request, 'scrapchef/editpost.html', context=context_dict)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, User=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('scrapchef:dashboard')  
    return redirect('scrapchef:dashboard')


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, User=request.user)
    if request.method == 'POST':

        caption = request.POST.get('caption')

        if not caption:
            messages.error(request, "Missing caption or media.")
            return redirect('scrapchef:dashboard')

        post.Caption = caption

        return redirect('scrapchef:dashboard')
    
    return redirect('scrapchef:dashboard')


def trending(request):
    # getting post objects and then getting the count of their reviews to sort by most reviewed
    post_list = Post.objects
    posts_with_ratings = []
    avg_ratings = []
    for post in post_list:
        posts_with_ratings.append((post, len(Review.objects.filter(Post_id=post.id))))
        avg_ratings.append(getPostAvgRatings(post))

    posts_with_ratings.sort(key=lambda x: x[1], reverse=True)
    sorted_posts = []
    for item in posts_with_ratings:
        sorted_posts.append(item[0])

    # context dict contains an array of posts ordered most reviewed to least reviewed
    # as well as a parallel array of dictionaries containing the avg ratings for each post
    context_dict = {}
    context_dict['posts'] = sorted_posts
    context_dict['avg_ratings'] = avg_ratings
    return render(request, 'scrapchef/trending.html', context=context_dict)


def bestmeals(request):
    post_list = Post.objects.all()
    sorted_posts, avg_ratings = orderByMealTastiness(post_list)

    if len(avg_ratings) != 0:
        sorted_posts.reverse()
        avg_ratings.reverse()

    # Add a new attribute to check if media is a URL
    for post in sorted_posts:
        if post.Media:    
            media_url = post.Media
            post.is_url = media_url.startswith("http") 
        else:
            post.is_url = False  
    context_dict = {
        'zip_post_ratings': zip(sorted_posts, avg_ratings),
    }

    return render(request, 'scrapchef/bestmeals.html', context=context_dict)


def worstmeals(request):
    post_list = Post.objects.all()
    sorted_posts, avg_ratings = orderByMealTastiness(post_list)

    # Add a new attribute to check if media is a URL
    for post in sorted_posts:
        if post.Media:
            media_url = post.Media
            post.is_url = media_url.startswith("http")
        else:
            post.is_url = False  

    context_dict = {
        'zip_post_ratings': zip(sorted_posts, avg_ratings),
    }

    return render(request, 'scrapchef/worstmeals.html', context=context_dict)


def recent(request):
    # context dict has a list of all posts ordered by date
    post_list = Post.objects.order_by('Date')
    
    avg_ratings = []
    for post in post_list:
        avg_ratings.append(getPostAvgRatings(post))

    context_dict = {}
    context_dict['posts'] = post_list
    context_dict['avg_ratings'] = avg_ratings
    return render(request, 'scrapchef/recent.html', context=context_dict)


def rating(request, post_name_slug):
    context_dict = {}
    try:
        post = Post.objects.get(slug=post_name_slug)
        context_dict['post'] = post
    except Post.DoesNotExist:
        context_dict['post'] = None

    if request.method == 'POST' and post:
        taste_val = request.POST.get('taste')
        struggle_val = request.POST.get('struggle')
        prep_val = request.POST.get('prep')

        if taste_val and struggle_val and prep_val:
            taste = int(taste_val)
            struggle = int(struggle_val)
            prep = int(prep_val)

            review = Review(Taste=taste, Struggle=struggle, Preparation=prep, Post=post)
            review.save()

            return redirect('scrapchef:feed')  # or wherever you want to go after rating

        # Optional: error message if something's missing
        context_dict['error'] = "Please select a value for all 3 categories before submitting."

    return render(request, 'scrapchef/rating.html', context=context_dict)
    
@login_required
def signout(request):
    auth_logout(request)
    return redirect(reverse('scrapchef:homepage'))

# ------------ Additional General Functions ----------- #

# function to get a list of all posts ordered by tastiness
def orderByMealTastiness(post_list):
    posts_with_ratings = []
    avg_ratings = []

    for post in post_list:

        reviews = Review.objects.filter(Post_id=post.id)

        # getting average tastiness rating of all reviews for this post
        total_tastiness = 0
        for review in reviews:
            total_tastiness += review.Taste

        if len(reviews) == 0:
            avg_tastiness = 0
        else:
            avg_tastiness = total_tastiness/len(reviews)

        avg_ratings.append((getPostAvgRatings(post), avg_tastiness))
        posts_with_ratings.append((post, avg_tastiness))

    avg_ratings.sort(key=lambda x: x[1])
    posts_with_ratings.sort(key=lambda x: x[1])

    sorted_posts = []
    sorted_ratings = []
    for i in range(len(posts_with_ratings)):
        sorted_posts.append(posts_with_ratings[i][0])
        sorted_ratings.append(avg_ratings[i][0])
        
    return sorted_posts, sorted_ratings


# function to calculate the average ratings of a given post
def getPostAvgRatings(post):
    avg_ratings = {}

    reviews = Review.objects.filter(Post_id=post.id)
    total_tastiness = 0
    total_struggle = 0
    total_prep = 0
    for review in reviews:
        total_tastiness += review.Taste
        total_struggle += review.Struggle
        total_prep += review.Preparation

    review_count = len(reviews)
    if review_count != 0:
        avg_ratings['avgTaste'] = round(total_tastiness/review_count)
        avg_ratings['avgStruggle'] = round(total_struggle/review_count)
        avg_ratings['avgPrep'] = round(total_prep/review_count)
    else:
        avg_ratings['avgTaste'] = 0
        avg_ratings['avgStruggle'] = 0
        avg_ratings['avgPrep'] = 0
    return avg_ratings 