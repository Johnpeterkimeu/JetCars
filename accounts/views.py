import email
from django.contrib.auth.hashers import make_password
from click import password_option
from django.http import HttpResponse
from django.shortcuts import redirect, render
from httplib2 import Authentication
from users.models import User
from accounts.models import Product
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

    


    



      

    

               

def shop (request):
    return render(request, 'shop.html')

def product(request):
    return render(request, 'product-details.html')


def checkout(request):
    return render(request, 'checkout.html')

def cart(request):
    return render(request, 'cart.html')

     
     
    
def order(request):
    if request.method == 'POST':
        firstname = request.post['firstname']
        lastname = request.post['lastname']
        Email = request.post['Email']


def  details(request,id):    
    product = Product.objects.get(id=id)
    context={}
    context["product"] = product

    return render(request,'product-details.html',context)

