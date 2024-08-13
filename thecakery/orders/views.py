from django.forms import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
from .models import Favorite, Cart, CartItem, Order, OrderItem, PaymentQR, ShippingAddress
from cakes.models import Cake, CakeSize
from party_accessories.models import PartyAccessory

@login_required
@require_POST
def toggle_favorite(request, cake_id):
    cake = Cake.objects.get(id=cake_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, cake=cake)

    if not created:
        favorite.delete()
        is_favorite = False
    else:
        is_favorite = True

    return JsonResponse({'success': True, 'is_favorite': is_favorite})

@login_required
def add_favorite(request, item_type, item_id):
    if item_type == 'cake':
        item = get_object_or_404(Cake, id=item_id)
        Favorite.objects.get_or_create(user=request.user, cake=item)
    elif item_type == 'accessory':
        item = get_object_or_404(PartyAccessory, id=item_id)
        Favorite.objects.get_or_create(user=request.user, accessory=item)
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def remove_favorite(request, item_type, item_id):
    if item_type == 'cake':
        item = get_object_or_404(Cake, id=item_id)
        Favorite.objects.filter(user=request.user, cake=item).delete()
    elif item_type == 'accessory':
        item = get_object_or_404(PartyAccessory, id=item_id)
        Favorite.objects.filter(user=request.user, accessory=item).delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def add_to_cart(request, item_type, item_id):
    quantity = request.POST.get('quantity', 1)  # Get the quantity from POST data, default to 1
    size_id = request.POST.get('size_id')  # Get the selected size ID from POST data

    try:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError("Quantity must be a positive integer.")
    except ValueError:
        messages.error(request, "Invalid quantity.")
        return redirect(request.META.get('HTTP_REFERER', 'home'))

    if item_type == 'cake':
        item = get_object_or_404(Cake, pk=item_id)
        size = None
        if size_id:
            size = get_object_or_404(CakeSize, pk=size_id, cake=item)
        else:
            # Automatically use the default size if none is selected
            size = CakeSize.objects.filter(size='small', cake=item).first()
            if not size:
                messages.error(request, "No default size available for this cake.")
                return redirect('cake_detail', cake_name=item.name)
    elif item_type == 'accessory':
        item = get_object_or_404(PartyAccessory, pk=item_id)
        size = None
    else:
        messages.error(request, "Invalid item type.")
        return redirect(request.META.get('HTTP_REFERER', 'home'))

    cart, created = Cart.objects.get_or_create(user=request.user)

    content_type = ContentType.objects.get_for_model(item)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        content_type=content_type,
        object_id=item_id,
        size=size,  # Include size in the query
        defaults={'quantity': quantity}
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    # Calculate the total price based on the updated quantity
    total_price = cart_item.get_price()

    size_info = size.size if size else 'N/A'
    messages.success(request, f"{quantity} x {item.name} ({size_info}) added to your cart.")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def remove_from_cart(request, cart_item_id):
    item_to_remove = get_object_or_404(CartItem, pk=cart_item_id)
    item_name = str(item_to_remove.content_object)
    item_to_remove.delete()

    messages.success(request, f"{item_name} removed from your cart.")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    data = {
        'cart_items': list(cart_items.values(
            'id',
            'content_type',
            'object_id',
            'quantity',
            'custom_text'
        ))
    }
    return JsonResponse(data)

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    qr_codes = PaymentQR.objects.all()

    if request.method == "POST":
        contact_number = request.POST.get('contact_number')
        shipping_address = request.POST.get('shipping_address')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        payment_method = request.POST.get('payment_method')
        payment_receipt = request.FILES.get('payment_receipt')  # For file uploads

        if not shipping_address:
            messages.error(request, "Shipping address is required.")
            return render(request, 'orders/checkout.html', {'cart': cart, 'qr_codes': qr_codes})

        if payment_method == 'qr_code' and not payment_receipt:
            messages.error(request, "Payment receipt is required for QR code payments.")
            return render(request, 'orders/checkout.html', {'cart': cart, 'qr_codes': qr_codes})

        # Calculate the total price
        total_price = cart.total_price()
        if payment_method == 'qr_code':
            payment_status = 'paid'
        else:
            payment_status = 'pending'

        # Create the Order
        user_address = ShippingAddress.objects.create(
            user=request.user,
            address=shipping_address,
            contact_number=contact_number,
            latitude=latitude,
            longitude=longitude,
            is_default=True
        )
        
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            destination=user_address,
            payment_method=payment_method,
            payment_status=payment_status,
            payment_receipt=payment_receipt if payment_method == 'qr_code' else None,
        )

        # Create OrderItems from CartItems
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                content_type=cart_item.content_type,
                object_id=cart_item.object_id,
                quantity=cart_item.quantity,
            )

        # Optionally, clear the cart after order placement
        cart.items.all().delete()

        # Redirect to a success page or order confirmation
        return redirect('order_confirmation', order_id=order.id)

    return render(request, 'orders/checkout.html', {'cart': cart, 'qr_codes': qr_codes})

@login_required
def create_order(request):
    cart = get_object_or_404(Cart, user=request.user)

    if not cart.items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart_detail')

    total_price = cart.total_price()

    try:
        with transaction.atomic():
            # Create the order instance
            order = Order.objects.create(
                user=request.user,
                total_price=total_price,
                destination='Sample destination',
                payment_status='Done'
            )

            # Transfer cart items to order items
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    content_type=cart_item.content_type,
                    object_id=cart_item.object_id,
                    quantity=cart_item.quantity
                )

            # Clear the cart items
            cart.items.all().delete()

        messages.success(request, "Order placed successfully!")
        return redirect('order_confirmation')

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('cart_detail')
    
@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = [
        {
            'name': item.content_object.name,
            'quantity': item.quantity,
            'price': item.content_object.price,
            'total_price': item.content_object.price * item.quantity
        }
        for item in order.order_items.all()
    ]
    payment_method_display = order.get_payment_method_display()
    payment_status_display = order.get_payment_status_display()
    shipping_status_display = order.get_shipping_status_display()

    return render(request, 'orders/order_confirmation.html', {
        'order': order,
        'order_items': order_items,
        'payment_method_display': payment_method_display,
        'payment_status_display': payment_status_display,
        'shipping_status_display': shipping_status_display,
    })

@login_required
def order_history(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    destination = order.destination
    order_items = OrderItem.objects.filter(order=order)
    context = {
        'order': order,
        'order_items': order_items,
        'destination_latitude': destination.latitude,
        'destination_longitude': destination.longitude,
    }
    return render(request, 'orders/order_detail.html', context)
