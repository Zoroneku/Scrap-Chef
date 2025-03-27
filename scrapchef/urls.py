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
    path('privacy-security/', views.privacy_security, name='privacy_security'),
    path('save/<int:post_id>/', views.save_post, name='save_post'),
    path('unsave_post/<int:post_id>/', views.unsave_post, name='unsave_post'),
    path('saved/', views.saved, name='saved'),
    path('post/', views.post, name='post'),
    path('editpost/<slug:post_name_slug>/', views.editpost, name='editpost'),
    path('upload/', views.upload_post, name='upload_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('rating/<slug:post_name_slug>/', views.rating, name='rating'),
    path('trending/', views.trending, name='trending'),
    path('bestmeals/', views.bestmeals, name='bestmeals'),
    path('worstmeals/', views.worstmeals, name='worstmeals'),
    path('recent/', views.recent, name='recent'),
    path('signout/', views.signout, name='signout'),
    path('edit-caption/<int:post_id>/', views.edit_caption, name='edit_caption'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
