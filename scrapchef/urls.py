from django.urls import path
from scrapchef import views  # Import views from your app

app_name = 'scrapchef'  # Allows namespace for URL names

urlpatterns = [
    path('', views.homepage, name='index'),  # Links to index.html
    path('login/', views.user_login, name='login'), # Links to auth.html (Login Mode)
    path('signup/', views.signup, name='signup'),  # Links to auth.html (Signup Mode)
    path('dashboard/', views.dashboard, name='dashboard'),  # Links to dashboard.html
    path('feed/', views.feed, name='feed'),  # Links to feed.html
    path('privacy/', views.privacy, name='privacy'),  # Add privacy.html later
    path('saved/', views.saved, name='saved'),  # Add saved_posts.html later
    path('post/', views.post, name='post'),  # Post Upload (Modal)
    path('editpost/', views.editpost, name='editpost'),  # Edit Post
    path('trending/', views.trending, name='trending'),  # Trending Feed
    path('bestmeals/', views.bestmeals, name='bestmeals'),  # Best Meals Feed
    path('worstmeals/', views.worstmeals, name='worstmeals'),  # Worst Meals Feed
    path('recent/', views.recent, name='recent'),  # Recent Meals Feed
    path('rating/', views.rating, name='rating'),  # Meal Rating (Modal)
    path('signout/', views.signout, name='signout'),  # Logout Page
]
