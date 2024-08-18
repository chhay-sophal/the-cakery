from django.urls import path
from .views import *

urlpatterns = [
    # Other URL patterns...
    path('dashboard/', index, name='staff_dashboard'),
    path('orders/', orders, name='orders'),
    path('orders/<int:order_id>/', order_detail, name='staff_order_detail'),
    path('orders/<int:order_id>/update/', update_order, name='update_order'),
    path('sales/', sales, name='sales'),
    path('reviews/', reviews, name='reviews'),
    path('stock/', stock, name='stock'),
    path('stock/product/add/', AddProductView.as_view(), name='add_product'),
    path('stock/product/<str:product_type>/<int:pk>/', product_detail, name='product_detail'),
    # path('stock/product/modify/<int:pk>/', ModifyProductView.as_view(), name='modify_product'),
    path('stock/product/modify/<str:product_type>/<int:pk>/', modify_product, name='modify_product'),
]
