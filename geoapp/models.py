from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.
class MallOwner(models.Model):
    pass

class Shop(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shop')
    shopId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    shopName = models.CharField(max_length=50)
    shopOwner = models.CharField(max_length=50, default="Blank")
    shopContact = models.CharField(max_length=50, default="9999999999")

    def __str__(self):
        return self.shopName


class Product(models.Model):
    productId = models.AutoField(primary_key=True)
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
    offerId = models.CharField(max_length = 20)
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    offeredby = models.ForeignKey(Shop,on_delete=models.CASCADE)
    offerprice = models.FloatField()

    def __str__(self):
        return self.offerId + self.product
    
