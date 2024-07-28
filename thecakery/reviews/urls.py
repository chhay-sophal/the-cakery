from django.urls import path
from . import views

urlpatterns = [
    path('<str:content_type>/<int:object_id>/', views.reviews, name='reviews'),
    path('add-cake-review/<int:cake_id>/', views.add_cake_review, name='add_cake_review'),
    path('add-accessory-review/<int:accessory_id>/', views.add_accessory_review, name='add_accessory_review'),
]