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
    path('edit_offer/<int:id>/',views.edit_offer,name="edit_offer"),
    path('productoffer/<int:pk>',views.ProductOffer,name='ProductOffer'),
    path('offer_toggle/<int:id>/',views.offer_toggle,name="offer_toggle"),
    path('offer/<int:pk>/',views.OfferByShop,name='offer'),
    path('offers/by-product/<int:product_id>/', views.OfferByProductView.as_view(), name='offer-by-product'),
    path('offers/by-shop/<int:shop_id>/', views.OfferByShopView.as_view(), name='offer-by-shop'),
    path('shops/by-location/',views.ShopByLocation.as_view(),name='shopbylocation'),
    path('offers/by-location/',views.OffersByLocation.as_view(),name='offersbylocation'),


    path('createmall/',views.createMall,name='createmall'),
    path('editmall/<mall_id>/',views.editmall,name='editmall'),
    path('deletemall/<mall_id>/',views.deletemall,name='deletemall'),
    path('addmalladmin/<int:mall_id>/',views.addmalladmin,name="addmalladmin"),
    path('viewmall/<int:mall_id>/',views.viewMall,name="viewmall"),
    path('listmall/',views.listMall,name='listmall'),
    path('addshopbymall/<int:mall_id>/',views.addshopbymall,name='addshopbymall'),
    path('getlocation/',views.LocationAPI.as_view(),name='getlocation'),
     path('shopsbymall/',views.shopsbymall,name='shopsbymall'),
     path('malls/',views.MallListView.as_view(),name="mallslist"),
     path('recordimpression/',views.RecordImpression.as_view(),name="recordimpression"),


     path('offer-impression-chart/', views.offer_impression_chart, name='offer_impression_chart'),
]
