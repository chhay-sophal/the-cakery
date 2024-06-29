from django.contrib import admin
from .models import Review

@admin.register(Review)
class CakeReviewAdmin(admin.ModelAdmin):
    list_display = ('cake', 'user', 'rating', 'created_at')