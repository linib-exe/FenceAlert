from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('createshop/',views.createshop,name='createshop'),
    path('login/',views.loginuser,name='login'),
    path('deleteshop/<str:pk>',views.deleteshop,name='deleteshop'),
    path('shop/<str:pk>',views.shopDetail,name='shopDetail'),
    path('editshop/<str:pk>',views.editshop,name='editshop'),
    path('addproduct/',views.addproduct,name='addproduct'),
    path('logout/',views.logoutuser,name='logout'),
    path('createoffer/<int:pk>',views.createOffer,name='createOffer'),
    path('productoffer/<int:pk>',views.ProductOffer,name='ProductOffer')
]
