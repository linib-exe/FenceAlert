
from rest_framework import serializers
from .models import Offer,Product,Mall,Shop,OfferImpression
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OfferSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    distance = serializers.CharField(max_length=100)
    class Meta:
        model = Offer
        fields = ['product','offeredby','offerTitle','offerprice','is_valid','distance']

class CustomOfferSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    productName = serializers.CharField()
    offerTitle = serializers.CharField()
    offerPrice = serializers.CharField()
    originalPrice = serializers.CharField()
    productImage = serializers.ImageField()
    shopName = serializers.CharField()

class CustomShopSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    shopName = serializers.CharField()
    shopContact = serializers.CharField()
    shopOwner = serializers.CharField()
    distance = serializers.CharField()

class ShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = '__all__'

class MallSerializer(serializers.ModelSerializer):
    shops = ShopSerializer(many=True)
    class Meta:
        model = Mall
        fields = '__all__'

class OfferImpressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferImpression
        fields = '__all__'
        # exclude = ['timestamp']
    