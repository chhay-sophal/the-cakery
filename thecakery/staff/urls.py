from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns...
    path('dashboard/', views.index, name='staff_dashboard'),
    path('orders/', views.orders, name='orders'),
    path('orders/<int:order_id>/', views.order_detail, name='staff_order_detail'),
    path('orders/<int:order_id>/update/', views.update_order, name='update_order'),
    path('sales/', views.sales, name='sales'),
    path('reviews/', views.reviews, name='reviews'),
    path('stock/', views.stock, name='stock'),
]
