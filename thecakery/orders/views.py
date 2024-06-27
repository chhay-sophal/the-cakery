from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cart, CartItem
from cakes.models import Cake
from party_accessories.models import PartyAccessory
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required

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
    return redirect('home')