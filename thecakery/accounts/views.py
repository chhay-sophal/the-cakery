from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeDoneView
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm
from orders.models import Order

@login_required
def profile(request):
    user = request.user
    orders = Order.objects.filter(user=user).exclude(shipping_status='delivered')
    return render(request, 'registration/profile.html', {'user': user, 'orders': orders})


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

