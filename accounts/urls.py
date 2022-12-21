from django.urls  import path

from .  import views

urlpatterns = [

    path('',views.home, name= 'index'),
    path('shop/',views.shop, name= 'SHOP'),
    path('product/', views.product, name = 'PRODUCTDETAILS'),
    path('cart/', views.cart, name= 'cart'),
    path('checkout/', views.checkout, name= 'checkout')
    ]
