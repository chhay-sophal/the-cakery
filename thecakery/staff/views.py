from pyexpat.errors import messages
from django.conf import settings
from django.forms import modelformset_factory
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Q, Sum
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from orders.models import Order, OrderItem
from accounts.models import UserProfile
from reviews.models import Review
from cakes.models import Cake, CakeImage, CakeSize
from party_accessories.models import PartyAccessory, PartyAccessoryImage
from django.views.generic import CreateView
from .forms import CakeForm, PartyAccessoryForm, UpdateOrderForm

def is_staff_user(user):
    return user.is_staff

@user_passes_test(is_staff_user)
def index(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    recent_orders = Order.objects.filter(
        ~Q(shipping_status__in=['delivered', 'cancelled'])
    ).order_by('-created_at')[:5]

    today = timezone.now().date()
    
    # Total Sales
    total_sales = Order.objects.aggregate(total=Sum('total_price'))['total'] or 0
    total_sales = float(total_sales)  # Ensure it's a number

    # Today's Sales
    today_sales = Order.objects.filter(created_at__date=today).aggregate(total=Sum('total_price'))['total'] or 0
    today_sales = float(today_sales)  # Ensure it's a number
    
    context = {
        'user': request.user,
        'user_profile': user_profile,
        'recent_orders': recent_orders,
        'today_sales': today_sales,
        'total_sales': total_sales,
    }
    
    return render(request, 'staff/index.html', context)

@user_passes_test(is_staff_user)
def orders(request):
    orders = Order.objects.filter(
        ~Q(shipping_status__in=['delivered', 'cancelled'])
    ).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'staff/orders.html', context)

@user_passes_test(is_staff_user)
def sales(request):
    orders = Order.objects.all().order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'staff/sales.html', context)

@user_passes_test(is_staff_user)
def update_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Check if the user is authorized to update the order
    if not request.user.is_staff and order.user != request.user:
        messages.error(request, "You are not authorized to update this order.")
        return redirect('staff_order_detail', order_id=order.id)

    if request.method == 'POST':
        form = UpdateOrderForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            form.save()
            return redirect('orders')
    else:
        form = UpdateOrderForm(instance=order)

    return render(request, 'staff/update_order.html', {'form': form, 'order': order})

@user_passes_test(is_staff_user)
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    destination = order.destination
    order_items = OrderItem.objects.filter(order=order)
    payment_method_display = order.get_payment_method_display()
    payment_status_display = order.get_payment_status_display()
    shipping_status_display = order.get_shipping_status_display()

    context = {
        'order': order,
        'order_items': order_items,
        'destination_latitude': destination.latitude,
        'destination_longitude': destination.longitude,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'payment_method_display': payment_method_display,
        'payment_status_display': payment_status_display,
        'shipping_status_display': shipping_status_display,
    }
    
    return render(request, 'staff/order_detail.html', context)

def reviews(request):
    # Fetch all reviews, ordered by the most recent
    reviews = Review.objects.order_by('-created_at')
    
    context = {
        'reviews': reviews,
    }
    
    return render(request, 'staff/reviews.html', context)
    # reviews = Review.objects.all()

    # # Prepare star rating data
    # for review in reviews:
    #     review.full_star_count = review.rating
    #     review.empty_star_count = 5 - review.rating

    # return render(request, 'staff/reviews.html', {'reviews': reviews})

def stock(request):
    cakes = Cake.objects.all()
    party_accessories = PartyAccessory.objects.all()
    return render(request, 'staff/stock.html', {
        'cakes': cakes,
        'party_accessories': party_accessories,
    })

class AddProductView(CreateView):
    template_name = "staff/add_product.html"

    def get(self, request, *args, **kwargs):
        cake_form = CakeForm(prefix="cake")
        accessory_form = PartyAccessoryForm(prefix="accessory")
        return render(request, self.template_name, {
            'cake_form': cake_form,
            'accessory_form': accessory_form,
        })

    def post(self, request, *args, **kwargs):
        cake_form = CakeForm(request.POST, request.FILES, prefix="cake")
        accessory_form = PartyAccessoryForm(request.POST, request.FILES, prefix="accessory")

        if cake_form.is_valid():
            cake = cake_form.save()
                
            # Save images
            for image in request.FILES.getlist('cake_form-images'):
                CakeImage.objects.create(cake=cake, image=image)
                
            return redirect('stock')

        if accessory_form.is_valid():
            accessory = accessory_form.save()
            for image in request.FILES.getlist('accessory_form-images'):
                PartyAccessoryImage.objects.create(accessory=accessory, image=image)
            return redirect('stock')

        return render(request, self.template_name, {
            'cake_form': cake_form,
            'accessory_form': accessory_form,
        })
    