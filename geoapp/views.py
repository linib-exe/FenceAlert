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
from .serializers import OfferSerializer,CustomShopSerializer,CustomOfferSerializer,MallSerializer,OfferImpressionSerializer
from django.db.models import F
from rest_framework.views import APIView
from .forms import ShopForm,ProductForm,MallForm,OfferForm

from .utils import calcdistance,getlocation

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


def listMall(request):
    malls = Mall.objects.all()
    context = {
        'malls':malls
    }
    return render(request,'mall/listmall.html',context)

def viewMall(request,mall_id):
    mall = Mall.objects.get(id=mall_id)
    shops = mall.shops.all()
    context = {
        'mall':mall,
        'shops':shops
    }
    return render(request,'mall/viewmall.html',context)
def createMall(request):
    form = MallForm()
    if request.method == "POST":
        form = MallForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listmall')
    context = {'form':form}
    return render(request,'mall/createmall.html',context)



def addshopbymall(request,mall_id):
    
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
                    createShop = Shop(user = user,shopName = shopName,shopOwner = shopOwner,shopContact = shopContact,latitude=latitude,longitude=longitude,mall_id=mall_id)
                    createShop.save()
                    messages.success(request,'Shop Created')
                    return redirect('listmall')
            else:
                    messages.success(request,'Username already taken')
        else:
            messages.success(request,'Fill username or email')

    mall = Mall.objects.get(id=mall_id)
    shops = mall.shops.all()
    lat = request.GET.get('lat')
    long = request.GET.get('long')
    coordinates = False
    if lat is not None and long is not None:
        coordinates = True
    context = {
       'coordinates':coordinates,
        'lat':lat,
        'long':long,
        'mall':mall,
        'shops':shops
    }
    return render(request,'mall/addshop.html',context)

def shopsbymall(request):
    mall_id = request.GET.get('mall_id')
    if mall_id is not None:
         shops = Shop.objects.filter(mall_id=mall_id)
    else:
        shops = Shop.objects.all()
   
    shops_list = []
    for shop in shops:
        shop_obj = {
            'shopName':shop.shopName,
            'latitude':shop.latitude,
            'longitude':shop.longitude,
        }
        shops_list.append(shop_obj)

    
    return JsonResponse(data={'shops':shops_list})
    

class LocationAPI(APIView):
     def get(self, request, *args, **kwargs):
        latitude = request.query_params.get('latitude', None)
        longitude = request.query_params.get('longitude', None)
        if latitude is not None and longitude is not None:
            print('Longitude: ',longitude,'Longitude: ',latitude)
            location = getlocation(lat=latitude,long=longitude)
            return Response({'location':location})



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

def deleteproduct(request,id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('home')

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



class MallListView(generics.ListAPIView):
    '''
    Returns all malls in the system
    '''
    queryset = Mall.objects.all()
    serializer_class = MallSerializer
    

class ShopByLocation(APIView):
    '''
    Return Shop by nearest location if latitude and longitude given
 
    </code>
    '''
    def get(self, request, *args, **kwargs):
        latitude = request.query_params.get('latitude', None)
        longitude = request.query_params.get('longitude', None)
        if latitude is not None and longitude is not None:
            print('Longitude: ',longitude,'Latitude: ',latitude)
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
            # shops = Shop.objects.all()
            # shop_list = []
            #TODO: find the mall and check within mall fence area
            malls = Mall.objects.all()
            mall_list = [] # list of mall 
            for mall in malls:
                
                user_mall_distance = round(calcdistance(user_lat,user_lon,mall.latitude,mall.longitude),2)
                print(user_mall_distance)
                # select the mall where the user is inside the fence
                if mall.fence_radius >= user_mall_distance:
                    #then add the mall to list
                    mall_with_distance = {

                    }
                    mall_with_distance['id'] = mall.id
                    mall_with_distance['mallName'] = mall.mallName
                    mall_with_distance['mallAddress'] = mall.mallAddress
                    mall_with_distance['fence_radius'] = mall.fence_radius
                    mall_with_distance['user_mall_distance'] = user_mall_distance
                    mall_list.append(mall_with_distance)
            if not len(mall_list)>0:
                return Response({'status':'error','message':'OUTSIDE THE MALL AREA'})
                
            sorted_mall_list = sorted(mall_list, key=lambda x: float(x['user_mall_distance']))
            # select the mall with least distance from the user
            selected_mall = sorted_mall_list[0] 
            selected_mall_object  = Mall.objects.get(id=selected_mall['id'])
            shops = Shop.objects.filter(mall = selected_mall_object)
            shop_list = [] # empty list of shops
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
            offers = Offer.objects.filter(offeredby_id=selected_shop['id'],is_valid=True).select_related('product','offeredby')
            print(offers)
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
            response_data['status'] = 'OK'
            response_data['message'] = "INSIDE MALL"
            response_data['shop_distance'] = selected_shop['distance']
            print(selected_shop['shopName'])
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
            response_data = {}
            response_data['status'] = 'OK'
            response_data['message'] = "USING DEFALUT LAT LONG"
            response_data['offers'] = serializer.data
            return Response(response_data)
        

class RecordImpression(generics.CreateAPIView):
    serializer_class = OfferImpressionSerializer



from django.db.models.functions import ExtractHour
from django.db.models import Count

def offer_impression_chart(request):
    # Query to aggregate impressions by hour
    impressions_by_hour = OfferImpression.objects.annotate(hour=ExtractHour('timestamp')).values('hour').annotate(count=Count('id')).order_by('hour')
    print(impressions_by_hour)
    # labels = [f'{hour}:00 - {hour + 1}:00' for hour in range(24)]
    # data = [impression['count'] if impression['hour'] in [point.hour for point in impressions_by_hour] else 0 for impression in impressions_by_hour]
    labels=None
    data=None
    return JsonResponse({'labels': labels, 'data': data}, safe=False)

# def offer_impression_chart(request):
#     impressions = OfferImpression.objects.all()
#     labels = [impression.timestamp.strftime('%Y-%m-%d %H:%M:%S') for impression in impressions]
#     data = list(range(1, len(labels) + 1))

#     return JsonResponse({'labels': labels, 'data': data}, safe=False)


def edit_offer(request,id):
    offer  = Offer.objects.get(id=id)
    form = OfferForm(instance=offer)
    if request.method == "POST":
        form = OfferForm(request.POST,instance=offer)
        if form.is_valid():
            form.save()
            return redirect(f"/productoffer/{offer.product_id}")
    context = {
        'form':form
    }
    return render(request,'edit_offer.html',context)

def offer_toggle(request,id):
    offer  = Offer.objects.get(id=id)
    if offer.is_valid == True:
        offer.is_valid = False
        offer.save()
        return redirect(f"/productoffer/{offer.product_id}")
    else:
        offer.is_valid = True
        offer.save()
        return redirect(f"/productoffer/{offer.product_id}")
