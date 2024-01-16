from django.forms import ModelForm
from .models import Shop,Product
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

