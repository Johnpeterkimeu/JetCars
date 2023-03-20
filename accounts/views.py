import email
import json
 


from sre_constants import CATEGORY, CATEGORY_DIGIT
from sre_parse import CATEGORIES
from unicodedata import category
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from click import password_option
from django.http import HttpResponse
from django.shortcuts import redirect, render
from httplib2 import Authentication
from users.models import User
from accounts.models import *
from django.contrib.auth.models import auth
# Create your views here.


def home (request):
    product = Product.objects.all()
    context={}
    context["products"] = product
    

    return render(request,'index.html' ,context)
def register(request):
    if request.method == 'POST':
        email= request.POST['email']
        
        password= request.POST['password']
        password3= request.POST['re-enter_password']
        
     
        if password == password3:
           # password = make_password(password)
           user=User.objects.create(email=email, password=password) 
           user.save()
           
           return redirect('login')
    return render(request, 'signup.html')        


def login(request):
    if request.method == 'POST':
       email = request.POST.get('email')
       password = request.POST.get('password')

       user= auth.authenticate(request,email=email, password=password)

       if user is not None:
            auth.login(request,user)
            return redirect('/')  
       else:
            return HttpResponse('email or password incorrect') 
    
    return render(request,'login.html')

def shipping(request):
    return render(request,'shipping.html')  

def save_data(request):
   
    #cart_total = order.get_cart_total()
  
   
    if request.method =='POST':
        Firstname=request.POST.get('Firstname')
        Lastname=request.POST.get('Lastname')
        payment=request.POST.get('AmountPaid')
      
        Checkout.objects.create( Firstname= Firstname, Lastname= Lastname,AmountPaid = payment)
    
    return redirect('/')
    
          
    


# def singleproduct(request, id):
#   context= {
#     'types': CATEGORY.objects.all(),
#     'products': Product.objects.filter(productid= id),
#     'incart':False,
#   }

#   if request.user.is_authenticated:
#      order = Order.objects.get_or_create(Customer=request.user.customer, _Complete=False)[0],
#      context['in_cart']= order.Orderitm_set.filter(product_productid = id).exists()
#      return render(request,'cart.html',context)



      

    

               

def shop (request):
    return render(request, 'shop.html')

def product(request):
    return render(request, 'product-details.html')


def checkout(request):
    context={}

    customer=request.user.customer  
    order,created =Order.objects.get_or_create(customer=customer,complete=False)
    context['order']=order
    return render(request, 'checkout.html',context)
    

def cart(request):
    context={}
    cart_items=Order_item.objects.all()
    customer=request.user.customer
    order,created =Order.objects.get_or_create(customer=customer,complete=False)
    #cart_total = order.get_cart_total()
    context['cart_items']=cart_items
    context['order']=order
   
    return render(request, 'cart.html',context)
    
     
     
    
def order(request):
    if request.method == 'POST':
        firstname = request.post['firstname']
        lastname = request.post['lastname']
        Email = request.post['Email']

    if request.user_is_authenticated:
        Customer.request.user.customer
        order, created=Order.objects.get_or_create(customer=Customer, complete=False)
        items=order.orderitem_set_all()
        cartItems=Order.get_cart_items
        types=CATEGORY.objects.all()
        prods= Product.objects.filter(productid=id)

        in_cart  = Order.orderitem_setfilter(product__productid=id).exists()



    else:

       types = category.objects.all()
       prods=product.objects.filter(productid=id)

       cartItems=[]

       in_cart = False


       return render(request,'cart.html',{'types':types,'prods':prods, 'in_cart':in_cart})

def  details(request,id):    
    product = Product.objects.get(id=id)
    context={}
    context["product"] = product

    return render(request,'product-details.html',context)

def UpdateItem(request):
    data=json.loads(request.body)
    productId= data['productId']
    action   = data['action']
    print('Action:',action)
    print('Product:',productId)

    customer=request.user.customer  
    print("thisis the ====",customer)
    product=Product.objects.get(id=productId)
    order,created =Order.objects.get_or_create(customer=customer,complete=False)

    orderItem,created =Order_item.objects.get_or_create(order=order,product=product)

    if action=='add':
       orderItem.quantity=(orderItem.quantity +1)
    elif action== 'remove':
       orderItem.quantity=(orderItem.quantity +1)

    orderItem.save()


    if orderItem.quantity <=0:
        orderItem.delete()

    return JsonResponse('item was added',safe=False)   

