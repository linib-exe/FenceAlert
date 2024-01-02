from django.contrib import admin
from .models import MallOwner,Shop,Product,Offer
class ShopAdmin(admin.ModelAdmin):
    list_display = ('shopName', 'shopOwner', 'shopContact')
# Register your models here.
admin.site.register(MallOwner)
admin.site.register(Shop,ShopAdmin)
admin.site.register(Product)
admin.site.register(Offer)
