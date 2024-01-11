from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login,authenticate
from django.contrib import messages
from django.contrib import messages
from rest_framework import generics
from .serializers import OfferSerializer



# Create your views here.
@login_required(login_url='login')
def home(request):
    if request.user.is_superuser:
        shops = Shop.objects.all()
        return render(request,'home.html',{'shops': shops})
    else:
        user = request.user 
        shop = Shop.objects.get(user = user)
        products = Product.objects.filter(productOwner = shop)
        return render(request,'home.html',{'products':products})

@login_required(login_url='login')
def createshop(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            shopName = request.POST.get('shopName')
            shopOwner = request.POST.get('shopOwner')
            shopContact = request.POST.get('shopContact')
            username = request.POST.get('Username')
            password = request.POST.get('Password')
            
            if username !=" " and password != "": 
                user = User(username = username)
                user.set_password(password)
                user.save()
                if user:
                    createShop = Shop(user = user,shopName = shopName,shopOwner = shopOwner,shopContact = shopContact)
                    createShop.save()
            else:
                messages.success(request,'Fill username or email')
                

        return render(request, 'createshop.html')
    else: 
        return redirect('/')

@login_required(login_url='login')
def deleteshop(request,pk):
    if request.user.is_superuser:
        shop = Shop.objects.get(pk = pk)
        shop.delete()
        return redirect('home')
    else:
        return redirect('/')

@login_required(login_url='login')
def addproduct(request):
    if request.method == 'POST':
        productName = request.POST.get('productName')
        productPrice = request.POST.get('productPrice')
        productCategory = request.POST.get('productCategory')
        current_shop = request.user.shop
        Product.objects.create(productName=productName,
                               productPrice=productPrice,
                               productCategory=productCategory,
                               productOwner = current_shop)
        return redirect('home')
    return render(request,'addproduct.html')


def shopDetail(request,pk): 
    if request.user.is_superuser:
        
        shop = Shop.objects.get(pk = pk)
        products = Product.objects.filter(productOwner = shop)
        return render(request,'shopDetails.html',{"shop":shop,'products':products})
        
    else:
        return redirect('/')
        
@login_required(login_url='login')
def editshop(request,pk):
    if request.user.is_superuser:
        shop = Shop.objects.get(pk = pk)
        if request.method == 'POST':
            shop.shopName = request.POST.get('shopName')
            shop.shopOwner = request.POST.get('shopOwner')
            shop.shopContact = request.POST.get('shopContact')
            shop.save()
            return redirect('home')
        return render(request,'editshop.html',{'shop':shop})
    else:
        return redirect('/')

def loginuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If user is valid, log in the user
            login(request, user)
            return redirect('home')  # Redirect to home page or desired URL
        else:
            # If authentication fails, return error message
            return render(request, 'login.html', {'error_message': 'Invalid login credentials!'})

    # If request method is not POST, render login page
    return render(request, 'login.html')

def logoutuser(request):
    logout(request)
    return redirect('home')



def createOffer(request,pk): 
    if request.method == "POST":
        title = request.POST.get('offerTitle')
        price = request.POST.get('offerprice')
        is_valid = request.POST.get('is_valid')
        product = Product.objects.get(pk = pk)
        shop = product.productOwner
        # print(type(is_valid))
        
        
        if is_valid == "on":
            offer = Offer(product = product,offeredby = shop,offerTitle = title,offerprice = price,is_valid = True)
            offer.save()
        else:
            offer = Offer(product = product,offeredby = shop,offerTitle = title,offerprice = price,is_valid = False)
            offer.save()

    return render(request,'createOffer.html',)


def ProductOffer(request,pk):
    product = Product.objects.get(pk = pk)
    offers = Offer.objects.filter(product = product)
    return render(request,'ProductOffer.html',{'offers':offers,'product':product})


def OfferByShop(request,pk): 
    shop = Shop.objects.get(pk = pk)
    offers = Offer.objects.filter(shop = shop)

    return render(request,'Offer.html',{"offers":offers})


class OfferByProductView(generics.ListAPIView):
    serializer_class = OfferSerializer

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Offer.objects.filter(product_id=product_id)

class OfferByShopView(generics.ListAPIView):
    serializer_class = OfferSerializer

    def get_queryset(self):
        shop_id = self.kwargs['shop_id']
        return Offer.objects.filter(offeredby_id=shop_id)
