from django.urls import path, include

from . import views

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
    path('', views.payment_view, name='payment'),
    path('callback/', views.payment_callback, name='payment_callback'),
    path('stk-status/', views.stk_status_view, name='stk_status'),
    path('subscribe/', views.subscribe, name='subscribe'),
    # path('cart/',views.cart_view, name='cart_items')
   
    ]
