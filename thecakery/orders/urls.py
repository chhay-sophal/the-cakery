from django.urls import path
from . import views

urlpatterns = [
    path('add-favorite/<str:item_type>/<int:item_id>/', views.add_favorite, name='add_favorite'),
    path('remove-favorite/<str:item_type>/<int:item_id>/', views.remove_favorite, name='remove_favorite'),
    path('add-to-cart/<str:item_type>/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('view-cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('create-order/', views.create_order, name='create_order'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('history/', views.order_history, name='order_history'),
    path('details/<int:order_id>/', views.view_order_details, name='order_details'),
]
