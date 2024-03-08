from django.contrib import admin
from .models import *
class ShopAdmin(admin.ModelAdmin):
    list_display = ('shopName', 'shopOwner', 'shopContact')
class ProductAdmin(admin.ModelAdmin):
    list_display = ('productOwner', 'productName', 'productPrice','productCategory')

admin.site.register(Shop,ShopAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Offer)
admin.site.register(Mall)
admin.site.register(OfferImpression)
