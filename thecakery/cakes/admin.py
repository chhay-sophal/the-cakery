from django.contrib import admin
from .models import Cake, CakeType, Flavour, CakeImage, CakeSize, TrendingCake, TrendingType

@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at', 'updated_at')

@admin.register(CakeType)
class CakeTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Flavour)
class FlavourAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(CakeImage)
class CakeImageAdmin(admin.ModelAdmin):
    list_display = ('cake', 'image', 'alt_text')

@admin.register(CakeSize)
class CakeSizeAdmin(admin.ModelAdmin):
    list_display = ('cake', 'size', 'additional_price')

@admin.register(TrendingType)
class TrendingTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(TrendingCake)
class TrendingCakeAdmin(admin.ModelAdmin):
    list_display = ('cake', 'trend_type', 'trend_score', 'description', 'created_at')
    list_filter = ('trend_type',)
    search_fields = ('cake__name',)