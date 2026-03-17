from django.contrib import admin
from .models import Recipe, Review

admin.site.register(Recipe)
admin.site.register(Review)