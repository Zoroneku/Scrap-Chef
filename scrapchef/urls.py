from django.urls import path
from scrapchef import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'scrapchef'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.login_view, name='login_view'),
    path('signup/', views.signup_view, name='signup_view'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('feed/', views.feed, name='feed'),
    path('privacy/', views.privacy, name='privacy'),
    path('saved/', views.saved, name='saved'),
    path('post/', views.post, name='post'),
    path('editpost/<slug:post_name_slug>/', views.editpost, name='editpost'),
    path('rating/<slug:post_name_slug>/', views.rating, name='rating'),
    path('trending/', views.trending, name='trending'),
    path('bestmeals/', views.bestmeals, name='bestmeals'),
    path('worstmeals/', views.worstmeals, name='worstmeals'),
    path('recent/', views.recent, name='recent'),
    path('signout/', views.signout, name='signout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
