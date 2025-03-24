from django.contrib import admin
from .models import UserProfile, Post, Review, List

# Register other models
admin.site.register(Post)
admin.site.register(Review)
admin.site.register(List)
admin.site.register(UserProfile)
