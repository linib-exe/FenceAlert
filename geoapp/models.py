from django.db import models
import uuid
from django.contrib.auth.models import User

class Mall(models.Model):
    mallName = models.CharField(max_length=100)
    mallAddress = models.CharField(max_length=255,blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    fence_radius = models.FloatField(default=500,help_text="Fence Radius in meters(m)") # in meters
    def __str__(self):
        return self.mallName

class Shop(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shop')
    shopName = models.CharField(max_length=50)
    shopOwner = models.CharField(max_length=50, default="Blank")
    shopContact = models.CharField(max_length=50, default="9999999999")
    latitude = models.CharField(max_length=100,default='0.0')
    mall = models.ForeignKey(Mall,on_delete=models.CASCADE,null=True,blank=True,related_name='shops')
    longitude = models.CharField(max_length=100,default="0.0")

    # fence_radius = models.FloatField()
    def __str__(self):
        return self.shopName


class Product(models.Model):
    productOwner = models.ForeignKey(Shop,on_delete = models.CASCADE)
    productName = models.CharField(max_length = 50)
    productPrice = models.FloatField()
    productCategory = models.CharField(max_length = 20,default="Electronics",choices = (
        ("Electronics","Electronics"),
        ("Fashion","Fashion"),
        ("Drinks","Drinks"),
        ("Furniture","Furniture")
    ))
    productImage = models.ImageField(upload_to='productImages/',default='productImages/product_placeholder.png',null=True)

    def __str__(self):
        return self.productName
    
class Offer(models.Model): 
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    offeredby = models.ForeignKey(Shop,on_delete=models.CASCADE)
    offerTitle = models.CharField(max_length = 500,blank = True,null = True)
    offerprice = models.FloatField()
    is_valid = models.BooleanField(default = False,null = True,blank = True)


class OfferImpression(models.Model):
    offer = models.ForeignKey(Offer,on_delete=models.CASCADE,related_name="impressions")
    timestamp = models.DateTimeField(auto_now=True,editable=True)
    status = models.CharField(max_length=20,blank=True)
    userdevice = models.CharField(max_length=255,blank=True)


    
