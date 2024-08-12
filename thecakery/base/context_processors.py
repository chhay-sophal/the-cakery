from django.shortcuts import get_object_or_404
from orders.models import Cart

def cart_context(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.items.all()
            total_price = cart.total_price()
        except Cart.DoesNotExist:
            cart_items = []
            total_price = 0
    else:
        cart_items = []
        total_price = 0

    return {
        'cart_items': cart_items,
        'total_price': total_price,
    }
