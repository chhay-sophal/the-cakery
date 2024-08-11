from django.contrib import admin
from django.urls import path
from .views import home_page, about, contact,catalog,chocolate,strawberry,vanilla,brownie,sign_up

urlpatterns = [
    path('', home_page, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('catalog/', catalog, name='catalog'),
    path('chocolate/', chocolate, name='chocolate'),
    path('strawberry/', strawberry, name='strawberry'),
    path('vanilla/', vanilla, name='vanilla'),
    path('brownie/', brownie, name='brownie'),
    path('sign_up/', sign_up, name='sign_up')
]
