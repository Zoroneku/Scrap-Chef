from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Post, Review, List

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

# Unregister the original User admin and register the customized one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register other models
admin.site.register(Post)
admin.site.register(Review)
admin.site.register(List)
