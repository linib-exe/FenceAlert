from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('ping/',views.pingPage,name="pingPage"),
    path('products/',views.productView,name='product'),
    path('',views.home,name='home'),
    path('createshop/',views.createshop,name='createshop'),
    path('login/',views.loginuser,name='login'),
    path('deleteshop/<str:pk>',views.deleteshop,name='deleteshop'),
    path('shop/<str:pk>',views.shopDetail,name='shopDetail'),
    path('editshop/<str:pk>',views.editshop,name='editshop'),
    path('addproduct/',views.addproduct,name='addproduct'),
    path('editproduct/<int:id>/',views.editproduct,name="editproduct"),
    path('deleteproduct/<int:id>/',views.deleteproduct,name="deleteproduct"),
    path('logout/',views.logoutuser,name='logout'),
    path('createoffer/<int:pk>',views.createOffer,name='createOffer'),
    path('productoffer/<int:pk>',views.ProductOffer,name='ProductOffer'),
    path('offer/<int:pk>/',views.OfferByShop,name='offer'),
    path('offers/by-product/<int:product_id>/', views.OfferByProductView.as_view(), name='offer-by-product'),
    path('offers/by-shop/<int:shop_id>/', views.OfferByShopView.as_view(), name='offer-by-shop'),
    path('shops/by-location/',views.ShopByLocation.as_view(),name='shopbylocation'),
    path('offers/by-location/',views.OffersByLocation.as_view(),name='offersbylocation')
]
