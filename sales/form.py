from django import forms
from django.forms import inlineformset_factory
from decimal import Decimal

from .models import Product, SalesModel, SalesDetailsModel
from user.models import Customer


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'vendor', 'catagory']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'vendor': forms.TextInput(attrs={'class': 'form-control'}),
            'catagory': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SalesForm(forms.ModelForm):
    
    class Meta:
        model = SalesModel
        fields = ['customer', 'subtotal', 'tax', 'grandtotal', 'amount_paid']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'subtotal': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True, 'id': 'id_subtotal'}),
            'tax': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True, 'id': 'id_tax'}),
            'grandtotal': forms.NumberInput(attrs={'class': 'form-control', 'readonly': True, 'id': 'id_grandtotal'}),
            'amount_paid': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.01, 'id': 'id_amount_paid'}),
        }
    



class SalesDetailsForm(forms.ModelForm):
    class Meta:
        model = SalesDetailsModel
        fields = ['product', 'quantity', 'price', 'total']
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-select product-select',
                'data-action': 'change->sales#updateProduct'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control quantity-input', 
                'min': 1,
                'data-action': 'change->sales#updateQuantity'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control price-input', 
                'readonly': True
            }),
            'total': forms.NumberInput(attrs={
                'class': 'form-control total-input', 
                'readonly': True
            }),
        }
    
    


SalesDetailsFormSet = inlineformset_factory(
    SalesModel,
    SalesDetailsModel,
    form=SalesDetailsForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True,
)