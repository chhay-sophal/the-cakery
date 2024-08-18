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
from cakes.models import Cake, CakeImage, CakeSize, Flavour
from party_accessories.models import PartyAccessory, PartyAccessoryImage
from django.views.generic import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.contenttypes.models import ContentType
from .forms import CakeForm, CakeImageForm, CakeSizeForm, FlavourForm, PartyAccessoryForm, PartyAccessoryImageForm, UpdateOrderForm, ModifyCakeForm, ModifyPartyAccessoryForm
from django.contrib.auth.decorators import login_required

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
    content_types = {
        'Cake': ContentType.objects.get_for_model(Cake).id,
        'PartyAccessory': ContentType.objects.get_for_model(PartyAccessory).id,
    }

    return render(request, 'staff/stock.html', {
        'cakes': cakes,
        'party_accessories': party_accessories,
        'content_types': content_types,
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
    
def product_detail(request, pk, product_type):
    if product_type == 'cake':
        object = get_object_or_404(Cake, pk=pk)
        product_type = 'cake'
    elif product_type == 'accessory':
        object = get_object_or_404(PartyAccessory, pk=pk)
        product_type = 'accessory'
    else:
        object = None
    
    context = {
        'object': object,
        'product_type': product_type,
    }
    return render(request, 'staff/product_detail.html', context)
    
@login_required
def modify_product(request, product_type, pk):
    if product_type == 'cake':
        product = get_object_or_404(Cake, pk=pk)
        form_class = CakeForm
    elif product_type == 'accessory':
        product = get_object_or_404(PartyAccessory, pk=pk)
        form_class = PartyAccessoryForm
    else:
        return redirect('product_stock')  # Redirect to stock if invalid product type

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_type=product_type, pk=product.pk)
    else:
        form = form_class(instance=product)

    return render(request, 'staff/modify_product.html', {
        'form': form,
        'product_type': product_type,
        'product': product
    })

@login_required
def manage_images(request, pk, product_type):
    if product_type == 'cake':
        obj = get_object_or_404(Cake, pk=pk)
        ImageModel = CakeImage
        form_class = CakeImageForm
    elif product_type == 'accessory':
        obj = get_object_or_404(PartyAccessory, pk=pk)
        ImageModel = PartyAccessoryImage
        form_class = PartyAccessoryImageForm
    else:
        return redirect('product_detail', pk=pk, product_type=product_type)
    
    if request.method == 'POST':
        if 'add_image' in request.POST:
            form = form_class(request.POST, request.FILES)
            if form.is_valid():
                new_image = form.save(commit=False)
                new_image.cake = obj if product_type == 'cake' else None
                new_image.accessory = obj if product_type == 'accessory' else None
                new_image.save()
        elif 'remove_image' in request.POST:
            image_id = request.POST.get('image_id')
            image = get_object_or_404(ImageModel, pk=image_id)
            image.delete()
        return redirect('product_detail', pk=pk, product_type=product_type)
    
    images = obj.images.all() if product_type == 'cake' else obj.images.all()
    form = form_class()

    context = {
        'object': obj,
        'images': images,
        'form': form,
        'product_type': product_type
    }
    return render(request, 'staff/manage_images.html', context)

@login_required
def manage_flavours(request, pk):
    cake = get_object_or_404(Cake, pk=pk)
    
    if request.method == 'POST':
        form = FlavourForm(request.POST, cake=cake)
        if 'add_flavour' in request.POST:
            if form.is_valid():
                flavour = form.cleaned_data['flavour']
                cake.flavours.add(flavour)
        elif 'remove_flavour' in request.POST:
            flavour_id = request.POST.get('flavour_id')
            flavour = get_object_or_404(Flavour, pk=flavour_id)
            cake.flavours.remove(flavour)
        return redirect('product_detail', pk=pk, product_type='cake')
    
    flavour_form = FlavourForm(cake=cake)
    
    context = {
        'object': cake,
        'flavour_form': flavour_form,
        'product_type': 'cake',
    }
    return render(request, 'staff/manage_flavours.html', context)

@login_required
def manage_sizes(request, pk):
    cake = get_object_or_404(Cake, pk=pk)
    
    if request.method == 'POST':
        if 'add_size' in request.POST:
            form = CakeSizeForm(request.POST)
            if form.is_valid():
                size = form.save(commit=False)
                size.cake = cake
                size.save()
        elif 'remove_size' in request.POST:
            size_id = request.POST.get('size_id')
            size = get_object_or_404(CakeSize, pk=size_id)
            size.delete()
        return redirect('manage_sizes', pk=pk)
    
    size_form = CakeSizeForm()
    
    context = {
        'cake': cake,
        'size_form': size_form,
        'sizes': cake.sizes.all(),
    }
    return render(request, 'staff/manage_sizes.html', context)