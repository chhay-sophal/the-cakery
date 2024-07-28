from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_all_accessories, name='view_all_accessories'),
    path('<int:item_id>/', views.get_accessory_details, name='get_accessory_details'),
]
