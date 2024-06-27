from django.contrib import admin
from .models import Cake, CakeType, CakeImage, CakeReview, CakeSize

@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at', 'updated_at')

@admin.register(CakeType)
class CakeTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(CakeImage)
class CakeImageAdmin(admin.ModelAdmin):
    list_display = ('cake', 'image', 'alt_text')

@admin.register(CakeReview)
class CakeReviewAdmin(admin.ModelAdmin):
    list_display = ('cake', 'user', 'rating', 'created_at')

@admin.register(CakeSize)
class CakeSizeAdmin(admin.ModelAdmin):
    list_display = ('cake', 'size', 'additional_price')