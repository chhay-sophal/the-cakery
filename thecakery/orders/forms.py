from django import forms

PAYMENT_CHOICES = [
    ('credit_card', 'Credit Card'),
    ('debit_card', 'Debit Card'),
    ('paypal', 'PayPal'),
    ('cash_on_delivery', 'Cash on Delivery'),
]

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(label='Shipping Address', max_length=255)
    payment_method = forms.ChoiceField(label='Payment Method', choices=PAYMENT_CHOICES, widget=forms.RadioSelect)