from django.urls import path

from .views import *


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('profile/', profile, name='profile'),
    path('logout/confirm/', logout_confirm, name='logout_confirm'),
]