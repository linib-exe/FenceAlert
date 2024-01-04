from django.db import models
import uuid
from django.contrib.auth.models import User



class Shop(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shop')
    shopName = models.CharField(max_length=50)
    shopOwner = models.CharField(max_length=50, default="Blank")
    shopContact = models.CharField(max_length=50, default="9999999999")

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

    def __str__(self):
        return self.productName
    
class Offer(models.Model): 
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    offeredby = models.ForeignKey(Shop,on_delete=models.CASCADE)
    offerTitle = models.CharField(max_length = 500,blank = True,null = True)
    offerprice = models.FloatField()
    is_valid = models.BooleanField(default = False,null = True,blank = True)

    
