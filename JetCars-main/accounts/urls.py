from django.urls import path, include

from . import views
from django.urls import path

urlpatterns = [

    path('',views.home, name= 'index'),
    path('shop/',views.shop, name= 'shop'),
    path('product/', views.product, name = 'product'),
    path('cart/', views.cart, name= 'cart'),
    path('checkout/', views.checkout, name= 'checkout'),
    path('register/', views.register, name= 'register'),
    path('login/', views.login, name= 'login'),
    path('logout/', views.logout, name= 'logout'),
    path('update_item/', views.UpdateItem, name= 'update_item'),   
    path('details/<id>/', views.details, name= 'product'),
    path('save_payment/', views.save_data, name= 'save_data'),
    path('payment/', views.payment_view, name='payment_view'),
    path('callback/', views.payment_callback, name='v'),
    path('stk-status/', views.stk_status_view, name='stk_status'),
    path('subscribe/', views.subscribe, name='subscribe'),
    
    
      
    # M-Pesa payment routes
    path('mpesa_payment/', views.mpesa_payment_view, name='mpesa_payment_view'),
    path('payment/', views.payment_view, name='payment'),
    path('stk_status/', views.stk_status_view, name='stk_status'),
    
    # This is the important callback URL that should match exactly what you've configured in Safaricom
    path('mpesa_callback/', views.payment_callback, name='mpesa_callback'),
    
    
    # path('mpesa_payment/', views.mpesa_payment_view, name='mpesa_payment_view'),
    # path('mpesa_callback/', views.mpesa_callback_view, name='mpesa_callback'),
    # path('payment/',views.payment_view, name='payment') 
    # path('cart/',views.cart_view, name='cart_items')
   
    ]
