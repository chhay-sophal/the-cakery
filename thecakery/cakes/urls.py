from django.urls import path
from . import views

urlpatterns = [
    path('<str:cake_name>/', views.get_cake_detail, name='cake_detial'),
]
