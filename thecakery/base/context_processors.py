from django.shortcuts import get_object_or_404
from orders.models import Cart
from cakes.models import Cake
from party_accessories.models import PartyAccessory

def cart_and_favorites_context(request):
    # Initialize variables
    cart_items = []
    total_price = 0
    cakes = []
    accessories = []

    if request.user.is_authenticated:
        # Fetch cart and cart items
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.items.all()
            total_price = cart.total_price()
        except Cart.DoesNotExist:
            pass  # Cart does not exist, no need to handle further
        
        # Fetch favorite items
        cakes = Cake.objects.filter(favorite__user=request.user)
        accessories = PartyAccessory.objects.filter(favorite__user=request.user)

    return {
        'cart_items': cart_items,
        'total_price': total_price,
        'favorite_cakes': cakes,
        'favorite_accessories': accessories,
    }