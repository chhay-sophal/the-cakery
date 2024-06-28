from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Cart, CartItem, Order, OrderItem
from .forms import CheckoutForm
from cakes.models import Cake
from party_accessories.models import PartyAccessory

@login_required
def add_to_cart(request, item_type, item_id):
    if item_type == 'cake':
        item = get_object_or_404(Cake, pk=item_id)
    elif item_type == 'accessory':
        item = get_object_or_404(PartyAccessory, pk=item_id)
    else:
        messages.error(request, "Invalid item type.")
        return redirect('home')

    cart, created = Cart.objects.get_or_create(user=request.user)

    content_type = ContentType.objects.get_for_model(item)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        content_type=content_type,
        object_id=item_id,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{item.name} added to your cart.")
    return JsonResponse({"message": f"{item.name} added to your cart."})

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
def remove_from_cart(request, cart_item_id):
    item_to_remove = get_object_or_404(CartItem, pk=cart_item_id)
    item_name = str(item_to_remove.content_object)
    item_to_remove.delete()

    messages.success(request, f"{item_name} removed from your cart.")
    return JsonResponse({"message": f"{item_name} added to your cart."})

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Process the form data (save shipping info, validate payment, etc.)
            # Redirect to create_order view after successful validation
            return redirect('create_order')
    else:
        form = CheckoutForm()
    
    context = {
        'form': form,
        'cart': cart,
    }
    return render(request, 'checkout.html', context)

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
def order_confirmation(request):
    context = {
        'message': 'Your order has been successfully placed. Thank you for shopping with us!'
    }
    return JsonResponse(context)

@login_required
def order_history(request):
    user_orders = Order.objects.filter(user=request.user)

    orders_data = []
    for order in user_orders:
        # Prepare the items associated with the order
        order_items = []
        for item in order.order_items.all():
            item_data = {
                'item_name': str(item.content_object),
                'quantity': item.quantity,
                'price_per_item': float(item.content_object.price),
                'total_price_for_item': float(item.content_object.price * item.quantity)
            }
            order_items.append(item_data)

        # Prepare the order data
        order_data = {
            'id': order.id,
            'total_price': float(order.total_price),
            'destination': order.destination,
            'payment_status': order.payment_status,
            'shipping_status': order.shipping_status,
            'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': order.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'items': order_items
        }
        orders_data.append(order_data)

    return JsonResponse(orders_data, safe=False)

@login_required
def view_order_details(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Constructing the response data
    order_details = {
        'order_id': order.id,
        'user': order.user.username,
        'total_price': float(order.total_price),  # Convert DecimalField to float for JSON serialization
        'destination': order.destination,
        'payment_status': order.payment_status,
        'shipping_status': order.shipping_status,
        'items': []
    }

    # Retrieve items and add them to the items list in the response
    for item in order.order_items.all():
        item_data = {
            'item_name': str(item.content_object),
            'quantity': item.quantity,
            'price_per_item': float(item.content_object.price),  # Convert DecimalField to float
            'total_price_for_item': float(item.content_object.price * item.quantity)  # Convert DecimalField to float
        }
        order_details['items'].append(item_data)

    order_details['created_at'] = order.created_at.isoformat()
    order_details['updated_at'] = order.updated_at.isoformat()

    return JsonResponse(order_details)
