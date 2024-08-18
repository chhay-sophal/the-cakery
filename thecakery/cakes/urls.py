from django.urls import path
from . import views
from .views import chocolate

urlpatterns = [
    path('', views.get_all_cakes, name='cakes_page'),
    path('<str:cake_name>/', views.get_cake_detail, name='cake_detail'),
    path('chocolate/', chocolate, name='chocolate')
]
