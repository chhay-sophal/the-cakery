from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from decimal import Decimal
from cakes.models import Cake, CakeSize
from party_accessories.models import PartyAccessory

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        return sum(item.get_price() for item in self.items.all())

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1)
    custom_text = models.CharField(max_length=25, blank=True, null=True)
    size = models.ForeignKey(CakeSize, null=False, blank=False, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.content_object} (x{self.quantity})"

    def clean(self):
        if self.custom_text and len(self.custom_text) > 25:
            raise ValidationError('Custom text cannot exceed 25 characters.')

    def save(self, *args, **kwargs):
        # Set default size if not provided
        if not self.size:
            default_size = CakeSize.objects.filter(size='small').first()
            if default_size:
                self.size = default_size
            else:
                raise ValidationError("Default size 'small' not found.")
        self.clean()
        super(CartItem, self).save(*args, **kwargs)

    def get_price(self):
        if isinstance(self.content_object, Cake):
            unit_price = self.content_object.price
            if self.size:
                unit_price += self.size.additional_price
        elif isinstance(self.content_object, PartyAccessory):
            unit_price = self.content_object.price
        else:
            return 0
        return unit_price * self.quantity

class Order(models.Model):
    SHIPMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    destination = models.CharField(max_length=255)
    payment_status = models.CharField(max_length=50)
    shipping_status = models.CharField(max_length=20, choices=SHIPMENT_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order by {self.user.username} on {self.created_at}"
    
    def calculate_total_price(self):
        total = sum(item.content_object.price * item.quantity for item in self.items.all())
        return total

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.content_object} (x{self.quantity})"