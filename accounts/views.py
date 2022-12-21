from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def home (request):
    return render(request,'index.html')

def register(request):
   if request.get == "POST":
      username = request.POST.get("username")
      Email  = request.POST.get("Mombile number or Email")
      password = request.POST.get("password")
      repeat = request.POST.get("repeat")


   if password == repeat:
     

def shop (request):
    return render(request, 'shop.html')

def product(request):
    return render(request, 'product-details.html')

def checkout(request):
    return render(request, 'checkout.html')

def cart(request):
    return render(request, 'cart.html')