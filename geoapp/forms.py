from django.forms import ModelForm
from .models import Shop,Product,Mall,Offer

class OfferForm(ModelForm):
    class Meta:
        fields = '__all__'
        exclude = ['product','is_valid']
        model = Offer


class ShopForm(ModelForm):
    class Meta:
        fields = '__all__'
        exclude = ['user']
        model = Shop

class ProductForm(ModelForm):
    class Meta:
        fields = '__all__'
        exclude = ['productOwner']
        model = Product


class MallForm(ModelForm):
    class Meta:
        fields = '__all__'
        model = Mall
