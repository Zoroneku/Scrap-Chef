from django.contrib import admin
from .models import User, Post, Review, List

# Register your models here.

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Review)
admin.site.register(List)
