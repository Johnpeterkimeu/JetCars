from django.urls  import path

from .  import views

urlpatterns = [

    path('',views.home, name= 'index'),
    path('shop/',views.shop, name= 'shop'),
    path('product/', views.product, name = 'product'),
    path('cart/', views.cart, name= 'cart'),
    path('checkout/', views.checkout, name= 'checkout'),
    path('register/', views.register, name= 'register'),
    path('login/', views.login, name= 'login'),    
    path('update_item/', views.UpdateItem, name= 'update_item'),   
    path('details/<id>/', views.details, name= 'product')


     
    
    ]
