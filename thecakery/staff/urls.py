from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns...
    path('', views.index, name='staff_dashboard'),
    path('order-tracking/', views.staff_order_tracking, name='staff_order_tracking'),
]
