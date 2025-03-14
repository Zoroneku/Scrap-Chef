from django.urls import path
from scrapchef import views

app_name = 'scrapchef'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('feed/', views.feed, name='feed'),
    path('privacy/', views.privacy, name='privacy'),
    path('saved/', views.saved, name='saved'),
    path('post/', views.post, name='post'),
    path('editpost/', views.editpost, name='editpost'),
    path('trending/', views.trending, name='trending'),
    path('bestmeals/', views.bestmeals, name='bestmeals'),
    path('worstmeals/', views.worstmeals, name='worstmeals'),
    path('recent/', views.recent, name='recent'),
    path('rating/', views.rating, name='rating'),
    path('signout/', views.signout, name='signout'),
]