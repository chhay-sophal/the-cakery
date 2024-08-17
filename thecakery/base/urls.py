from django.contrib import admin
from django.urls import path
from .views import home_page, about, contact,catalog

urlpatterns = [
    path('', home_page, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('catalog/', catalog, name='catalog'),
]
