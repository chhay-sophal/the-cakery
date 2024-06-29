from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_object', 'user', 'rating', 'created_at')
    list_filter = ('content_type', 'created_at')
    search_fields = ('user__username', 'comment')
    date_hierarchy = 'created_at'

    def content_object(self, obj):
        return obj.content_object.name  # Adjust this based on your model structure
    content_object.short_description = 'Content Object'