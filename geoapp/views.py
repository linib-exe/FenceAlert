from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login,authenticate
from django.contrib import messages
from django.contrib import messages
from rest_framework import generics
from rest_framework.response import Response
from .serializers import OfferSerializer,CustomShopSerializer,CustomOfferSerializer
from django.db.models import F
from rest_framework.views import APIView
from .forms import ShopForm,ProductForm
def pingPage(request):
    return JsonResponse({'status':'OK'},safe=False)
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
        # form = ShopForm()
        if request.method == 'POST':
            shopName = request.POST.get('shopName')
            shopOwner = request.POST.get('shopOwner')
            shopContact = request.POST.get('shopContact')
            username = request.POST.get('Username')
            password = request.POST.get('Password')
            latitude = request.POST.get('shopLatitude')
            longitude = request.POST.get('shopLongitude')
            if username !=" " and password != "": 
                if not User.objects.filter(username=username).exists():
                    user = User(username = username)
                    user.set_password(password)
                    user.save()
                    if user:
                        createShop = Shop(user = user,shopName = shopName,shopOwner = shopOwner,shopContact = shopContact,latitude=latitude,longitude=longitude)
                        createShop.save()
                        messages.success(request,'Shop Created')
                else:
                     messages.success(request,'Username already taken')
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
        productImage = request.FILES.get('productImage')
        current_shop = request.user.shop
        if productImage is not None:
            Product.objects.create(productName=productName,
                                productPrice=productPrice,
                                productCategory=productCategory,
                                productOwner = current_shop,productImage=productImage)
        else:
            Product.objects.create(productName=productName,
                                productPrice=productPrice,
                                productCategory=productCategory,
                                productOwner = current_shop,)

        return redirect('home')
    return render(request,'addproduct.html')


@login_required(login_url='login')
def editproduct(request,id):
    product = Product.objects.get(id=id)
    form = ProductForm(instance = product)
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES,instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.productOwner = request.user.shop
            product.save()      
            messages.success(request,'Product Updated')
        # productName = request.POST.get('productName')
        # productPrice = request.POST.get('productPrice')
        # productCategory = request.POST.get('productCategory')
        # productImage = request.FILES.get('productImage')
        # current_shop = request.user.shop
        # if productImage is not None:
        #     print('image yes')
        #     Product.objects.create(productName=productName,
        #                         productPrice=productPrice,
        #                         productCategory=productCategory,
        #                         productOwner = current_shop,productImage=productImage)
        # else:
        #     print('no image')
        #     Product.objects.create(productName=productName,
        #                         productPrice=productPrice,
        #                         productCategory=productCategory,
        #                         productOwner = current_shop,)
        return redirect('home')
    context = {
        'form':form,
        'product':product
    }
    return render(request,'editproduct.html',context)


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
            shop.latitude = request.POST.get('shopLatitude')
            shop.longitude = request.POST.get('shopLongitude')
            shop.save()
            messages.success(request,'Shop Updated')
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
        return Offer.objects.filter(offeredby_id=shop_id).select_related('product')

from django.http import JsonResponse
import time
def productView(request):
    data = [
  {
    "name": "Widget A",
    "markedPrice": 25.0,
    "salePrice": 19.99,
    "shopName": "Tech Emporium"
  },
  {
    "name": "Gadget X",
    "markedPrice": 45.0,
    "salePrice": 39.99,
    "shopName": "Electro Depot"
  },
  {
    "name": "Super Gizmo",
    "markedPrice": 30.0,
    "salePrice": 24.99,
    "shopName": "Innovation Hub"
  },
  {
    "name": "Tech Marvel",
    "markedPrice": 60.0,
    "salePrice": 49.99,
    "shopName": "Digital Haven"
  }
]
    time.sleep(0.5)

    return JsonResponse(data,safe=False)

#TODO: this function calculates distance between two geological coordinates
from geopy.distance import geodesic
def calcdistance(lat1,long1,lat2,long2):
    return geodesic((lat1,long1),(lat2,long2)).meters

class ShopByLocation(APIView):
    '''
    Return Shop by nearest location if latitude and longitude given
 
    </code>
    '''
    def get(self, request, *args, **kwargs):
        latitude = request.query_params.get('latitude', None)
        longitude = request.query_params.get('longitude', None)
        if latitude is not None and longitude is not None:
            print('Longitude: ',longitude,'Longitude: ',latitude)
            user_lat = latitude
            user_lon = longitude
            shops = Shop.objects.all()
            shop_list = []
            
            for shop in shops:
                distance = round(calcdistance(user_lat,user_lon,shop.latitude,shop.longitude),2)
                shop_with_distance = {}
                shop_with_distance['id'] = shop.id
                shop_with_distance['shopName'] = shop.shopName
                shop_with_distance['shopContact'] = shop.shopContact
                shop_with_distance['shopOwner'] = shop.shopOwner
                shop_with_distance['distance'] = distance
                shop_list.append(shop_with_distance)
            sorted_shop_list = sorted(shop_list, key=lambda x: float(x['distance']))
            selected_shop = sorted_shop_list[0]
            serializer = CustomShopSerializer(sorted_shop_list,many=True)
            #TODO:

            return Response(serializer.data)
        
            
        else :
            
            shops = Shop.objects.all()
            shop_list = []
            
            for shop in shops:
                distance = "0.0"
                shop_with_distance = {}
                shop_with_distance['id'] = shop.id
                shop_with_distance['shopName'] = shop.shopName
                shop_with_distance['shopContact'] = shop.shopContact
                shop_with_distance['shopOwner'] = shop.shopOwner
                shop_with_distance['distance'] = distance
                shop_list.append(shop_with_distance)
            sorted_shop_list = sorted(shop_list, key=lambda x: float(x['distance']))
            # selected_shop = sorted_shop_list[0]
            serializer = CustomShopSerializer(sorted_shop_list,many=True)


            # for shop in shops:
            #     print(shop.distance)

            return Response(serializer.data)

        
class OffersByLocation(APIView):
    def get(self, request, *args, **kwargs):
        latitude = request.query_params.get('latitude', None)
        longitude = request.query_params.get('longitude', None)
        if latitude is not None and longitude is not None:
            print('Longitude: ',longitude,'Longitude: ',latitude)

            user_lat = latitude
            user_lon = longitude
            shops = Shop.objects.all()
            shop_list = []
            
            for shop in shops:
                distance = round(calcdistance(user_lat,user_lon,shop.latitude,shop.longitude),2)
                shop_with_distance = {}
                shop_with_distance['id'] = shop.id
                shop_with_distance['shopName'] = shop.shopName
                shop_with_distance['shopContact'] = shop.shopContact
                shop_with_distance['shopOwner'] = shop.shopOwner
                shop_with_distance['distance'] = distance
                shop_list.append(shop_with_distance)
            sorted_shop_list = sorted(shop_list, key=lambda x: float(x['distance']))
            selected_shop = sorted_shop_list[0]
            offers = Offer.objects.filter(offeredby_id=selected_shop['id']).select_related('product','offeredby')

            offers_list = []
            for offer in offers:
                offer_obj = {}
                offer_obj['id'] = offer.id
                offer_obj['productName'] = offer.product.productName
                offer_obj['offerTitle'] = offer.offerTitle
                offer_obj['offerPrice'] = offer.offerprice
                offer_obj['originalPrice'] = offer.product.productPrice
                offer_obj['shopName'] = offer.offeredby.shopName
                offer_obj['productImage'] = offer.product.productImage
                offers_list.append(offer_obj)
            serializer = CustomOfferSerializer(offers_list,many=True)
            offerdata = serializer.data
            response_data = {}
            response_data['shop_distance'] = selected_shop['distance']
            response_data['offers'] = offerdata
            return Response(response_data)

        #TODO:
        else:
            user_lat = "26.797206"
            user_lon = "87.291943"
            shops = Shop.objects.all()
            shop_list = []
            
            for shop in shops:
                distance = calcdistance(user_lat,user_lon,shop.latitude,shop.longitude)
                shop_with_distance = {}
                shop_with_distance['id'] = shop.id
                shop_with_distance['shopName'] = shop.shopName
                shop_with_distance['shopContact'] = shop.shopContact
                shop_with_distance['shopOwner'] = shop.shopOwner
                shop_with_distance['distance'] = distance
                shop_list.append(shop_with_distance)
            sorted_shop_list = sorted(shop_list, key=lambda x: float(x['distance']))
            selected_shop = sorted_shop_list[0]
            offers = Offer.objects.filter(offeredby_id=selected_shop['id']).select_related('product','offeredby')

            offers_list = []
            for offer in offers:
                offer_obj = {}
                offer_obj['id'] = offer.id
                offer_obj['productName'] = offer.product.productName
                offer_obj['offerTitle'] = offer.offerTitle
                offer_obj['offerPrice'] = offer.offerprice
                offer_obj['originalPrice'] = offer.product.productPrice
                offer_obj['shopName'] = offer.offeredby.shopName
                offer_obj['productImage'] = offer.product.productImage

                offers_list.append(offer_obj)

            serializer = CustomOfferSerializer(offers_list,many=True)
            return Response(serializer.data)





