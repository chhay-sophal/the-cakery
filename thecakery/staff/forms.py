# forms.py
from django import forms
from orders.models import Order

class UpdateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_status', 'payment_status', 'payment_method', 'payment_receipt']
        widgets = {
            'shipping_status': forms.Select(attrs={'class': 'form-control'}),
            'payment_status': forms.Select(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'payment_receipt': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
