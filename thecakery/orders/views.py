from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
from .models import Favorite, Cart, CartItem, Order, OrderItem
from .forms import CheckoutForm
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
