from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('createshop/',views.createshop,name='createshop'),
    path('login/',views.loginuser,name='login'),
    path('deleteshop/<str:pk>',views.deleteshop,name='deleteshop'),
    path('editshop/<str:pk>',views.editshop,name='editshop'),
    path('addproduct/',views.addproduct,name='addproduct'),
    path('logout/',views.logoutuser,name='logout')
]
