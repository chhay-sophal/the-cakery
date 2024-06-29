from django.urls import path
from . import views

urlpatterns = [
    path('cake/<int:cake_id>/', views.cake_reviews, name='cake_reviews'),
]