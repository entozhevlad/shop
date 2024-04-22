from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    delivery_method = forms.ChoiceField(choices=Order.DELIVERY_CHOICES,
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']