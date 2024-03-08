from django.forms import ModelForm
from .models import Shop,Product,Mall,Offer

class OfferForm(ModelForm):
    class Meta:
        fields = '__all__'
        exclude = ['product','is_valid','detail_exp_count','dismissed_count','received_count']
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
        exclude =['mall_admin']
        model = Mall
