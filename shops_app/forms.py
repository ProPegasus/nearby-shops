from django import forms
from .models import Shop


class ShopForm(forms.ModelForm):
    
    """
    Model form to facilitate the addition of more shops.

    """

    class Meta:
        model = Shop
        fields = '__all__'