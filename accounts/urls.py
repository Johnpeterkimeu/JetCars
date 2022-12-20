from django.urls  import path

from .  import views

urlpatterns = [
    path('',views.home, name= 'index'),
    path('',views.shop, name= 'SHOP'),
    path('', views.Product, name = 'PRODUCTDETAILS'),
    path('',views.cart, name= 'CART'),
    path('', views.checkout, name= 'CHECKOUT')
    ]
