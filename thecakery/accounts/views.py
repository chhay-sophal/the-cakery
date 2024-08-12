from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView

@login_required
def profile(request):
    return render(request, 'registration/profile.html', {'user': request.user})

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def logout_confirm(request):
    return render(request, 'registration/logout_confirm.html')
