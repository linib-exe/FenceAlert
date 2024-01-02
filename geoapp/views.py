from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Shop,Product
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout,login,authenticate
# Create your views here.
@login_required(login_url='login')
def home(request):
    shops = Shop.objects.all()
    return render(request,'home.html',{'shops': shops})

@login_required(login_url='login')
def createshop(request):
    if request.method == 'POST':
        shopName = request.POST.get('shopName')
        shopOwner = request.POST.get('shopOwner')
        shopContact = request.POST.get('shopContact')
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        print(username)
        # Create a User instance
        user = User(username=username, password=password)
        user.save()
        if user:
        # Create a Shop instance associated with the created User
            Shop.objects.create(user=user,  # Link the Shop to the created User
                                shopName=shopName,
                                shopOwner=shopOwner,
                                shopContact=shopContact)
            
            return redirect('home')  # Redirect to the desired URL after successful creation
    
    return render(request, 'createshop.html')

@login_required(login_url='login')
def deleteshop(request,pk):
    shop = Shop.objects.get(shopId = pk)
    shop.delete()
    return redirect('home')

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

@login_required(login_url='login')
def editshop(request,pk):
    shop = Shop.objects.get(shopId = pk)
    if request.method == 'POST':
        shop.shopName = request.POST.get('shopName')
        shop.shopOwner = request.POST.get('shopOwner')
        shop.shopContact = request.POST.get('shopContact')
        shop.save()
        return redirect('home')
    return render(request,'editshop.html',{'shop':shop})

def loginuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

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
