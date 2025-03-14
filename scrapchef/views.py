from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from scrapchef.models import Post, Review


def homepage(request):
    return render(request, 'scrapchef/homepage.html')


@login_required
def dashboard(request):
    context_dict = {}
    context_dict['username'] = user.Username
    context_dict['occupation'] = user.Occupation
    context_dict['posts'] = Post.objects.filter(Username=user.Username)
    context_dict['pfp'] = user.ProfilePhoto

    return render(request, 'scrapchef/dashboard.html', context=context_dict)


def feed(request):
    # context dict has a list of all posts ordered by date
    post_list = Post.objects.order_by('date')
    avg_ratings = []
    for post in post_list:
        avg_ratings.append(getPostAvgRatings(post))

    context_dict = {}
    context_dict['posts'] = post_list
    context_dict['avg_ratings'] = avg_ratings
    return render(request, 'scrapchef/feed.html', context=context_dict)


def privacy(request):
    # add stuff here
    return render(request, 'scrapchef/privacy.html')


def saved(request):
    # add stuff here
    return render(request, 'scrapchef/saved.html')


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


def trending(request):
    # getting post objects and then getting the count of their reviews to sort by most reviewed
    post_list = Post.objects
    posts_with_ratings = []
    avg_ratings = []
    for post in post_list:
        posts_with_ratings.append((post, len(Review.objects.filter(PostID=post.postID))))
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
    post_list = Post.objects
    sorted_posts, avg_ratings = orderByMealTastiness(post_list)


    # context dict contains a list of posts ordered most to least tasty
    context_dict = {}
    context_dict['posts'] = sorted_posts
    context_dict['avg_ratings'] = avg_ratings
    return render(request, 'scrapchef/bestmeals.html', context=context_dict)


def worstmeals(request):
    post_list = Post.objects
    sorted_posts, avg_ratings = orderByMealTastiness(post_list)

    # context dict contains a list of posts ordered least to most tasty
    context_dict = {}
    context_dict['posts'] = sorted_posts
    context_dict['avg_ratings'] = avg_ratings
    return render(request, 'scrapchef/worstmeals.html', context=context_dict)


def recent(request):
    # context dict has a list of all posts ordered by date
    post_list = Post.objects.order_by('date')
    
    avg_ratings = []
    for post in post_list:
        avg_ratings.append(getPostAvgRatings(post))

    context_dict = {}
    context_dict['posts'] = post_list
    context_dict['avg_ratings'] = avg_ratings
    return render(request, 'scrapchef/recent.html', context=context_dict)


def rating(request, post_name_slug):
    # context dict has simply the post that is being reviewed
    context_dict = {}
    try:
        post = Post.objects.get(slug=post_name_slug)
        context_dict['post'] = post
    except Post.DoesNotExist:
        context_dict['post'] = None

    return render(request, 'scrapchef/rating.html', context=context_dict)


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
    

def signup(request):
    return render(request, 'scrapchef/signup.html')
    

@login_required
def signout(request):
    logout(request)
    return redirect(reverse('scrapchef:homepage'))


# ------------ Additional General Functions ----------- #

# function to get a list of all posts ordered by tastiness
def orderByMealTastiness(post_list):
    posts_with_ratings = []
    avg_ratings = []

    for post in post_list:

        avg_ratings.append(getPostAvgRatings(post))

        # getting average tastiness rating of all reviews for this post
        total_tastiness = 0
        for review in Review.objects.filter(PostID=post.postID):
            total_tastiness += review.Taste

        avg_tastiness = total_tastiness/len(Review.objects.filter(PostID=post.postID))

        posts_with_ratings.append((post, avg_tastiness))

    posts_with_ratings.sort(key=lambda x: x[1])
    sorted_posts = []
    for item in posts_with_ratings:
        sorted_posts.append(item[0])
        
    return sorted_posts, avg_ratings


# function to calculate the average ratings of a given post
def getPostAvgRatings(post):
    avg_ratings = {}

    total_tastiness = 0
    total_struggle = 0
    total_prep = 0
    for review in Review.objects.filter(PostID=post.postID):
        total_tastiness += review.Taste
        total_struggle += review.Struggle
        total_prep += review.Preparation

    review_count = len(Review.objects.filter(PostID=post.postID))
    avg_ratings['avgTaste'] = total_tastiness/review_count
    avg_ratings['avgStruggle'] = total_struggle/review_count
    avg_ratings['avgPrep'] = round(total_prep/review_count)

    return avg_ratings