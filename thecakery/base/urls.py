from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', home_page, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('catalog/', catalog, name='catalog'),
    path('birthday/', birthday, name='birthday'),
    path('wedding/', wedding, name='wedding'),
    path('anniversary/', anniversary, name='anniversary'),
    path('celebration/', celebration, name='celebration'),
    path('sign_up/', sign_up, name='sign_up'),
    path('dessert/', dessert, name='dessert'),
    path('accessory/', accessory_list, name='accessory'),
]
