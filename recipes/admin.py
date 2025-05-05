from django.contrib import admin
from . import models
from django.contrib import admin
from .models import Rating

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user', 'stars', 'created_at')
    list_filter = ('stars', 'created_at')
    search_fields = ('recipe__title', 'user__username')


# Register your models here.
admin.site.register(models.Recipe)