from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_cakes, name='cakes_page'),
    path('<str:cake_name>/', views.get_cake_detail, name='cake_detial'),
]
