from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def home (request):
    return render(request,'index.html')


def shop (request):
    return render(request, 'shop.html')

def Product(request):
    return render(request, 'product-details.html')

def checkout(request):
    return render(request, 'checkout.html')

def cart(request):
    return render(request, 'cart.html')