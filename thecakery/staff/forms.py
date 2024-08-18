# forms.py
from django import forms
from django.forms import modelformset_factory
from orders.models import Order
from cakes.models import Cake, CakeImage, Flavour, CakeSize
from party_accessories.models import PartyAccessory, PartyAccessoryImage


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

CakeSizeFormSet = modelformset_factory(CakeSize, fields=('size', 'additional_price'), extra=1)

class CakeForm(forms.ModelForm):
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        required=False
    )
    flavours = forms.ModelMultipleChoiceField(
        queryset=Flavour.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )

    class Meta:
        model = Cake
        fields = ['name', 'description', 'cake_type', 'flavours', 'price', 'stock', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter cake name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description', 'rows': 4}),
            'cake_type': forms.Select(attrs={'class': 'form-select'}),
            # 'flavours': forms.SelectMultiple(attrs={
            #     'class': 'form-control selectpicker',
            #     'data-live-search': 'true',
            #     'data-style': 'btn-outline-primary',
            #     'data-width': '100%',
            #     'data-selected-text-format': 'count > 3'  # Show selected count if more than 3
            # }),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter stock quantity'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

class PartyAccessoryForm(forms.ModelForm):
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        required=False
    )

    class Meta:
        model = PartyAccessory
        fields = ['name', 'description', 'price', 'stock']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter accessory name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter stock quantity'}),
        }

class ModifyCakeForm(forms.ModelForm):
    class Meta:
        model = Cake
        fields = ['name', 'description', 'cake_type', 'flavours', 'price', 'stock', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['flavours'].widget = forms.CheckboxSelectMultiple()
        self.fields['images'].widget = forms.ClearableFileInput(attrs={'multiple': True})

class ModifyPartyAccessoryForm(forms.ModelForm):
    class Meta:
        model = PartyAccessory
        fields = ['name', 'description', 'price', 'stock']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['images'].widget = forms.ClearableFileInput(attrs={'multiple': True})

class CakeImageForm(forms.ModelForm):
    class Meta:
        model = CakeImage
        fields = ['image', 'alt_text']

class PartyAccessoryImageForm(forms.ModelForm):
    class Meta:
        model = PartyAccessoryImage
        fields = ['image', 'alt_text']

class FlavourForm(forms.Form):
    def __init__(self, *args, **kwargs):
        cake = kwargs.pop('cake')  # Extract the cake object from kwargs
        super().__init__(*args, **kwargs)
        self.fields['flavour'].queryset = Flavour.objects.exclude(cakes=cake)
    
    flavour = forms.ModelChoiceField(
        queryset=Flavour.objects.none(),  # Default queryset, will be set in __init__
        widget=forms.Select,
        empty_label="Select a flavour"
    )

class CakeSizeForm(forms.ModelForm):
    class Meta:
        model = CakeSize
        fields = ['size', 'additional_price']