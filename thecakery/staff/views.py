from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from orders.models import Order
from accounts.models import UserProfile

def is_staff_user(user):
    return user.is_staff

@user_passes_test(is_staff_user)
def index(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    recent_orders = Order.objects.all().order_by('-created_at')[:5]
    
    context = {
        'user': request.user,
        'user_profile': user_profile,
        'recent_orders': recent_orders,
    }
    
    return render(request, 'staff/index.html', context)

@user_passes_test(is_staff_user)
def staff_order_tracking(request):
    orders = Order.objects.all().order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'staff/order_tracking.html', context)
