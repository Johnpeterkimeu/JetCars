import base64
import email
import json
import os
import re
import requests 
from requests.auth import HTTPBasicAuth
from decimal import Decimal

from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from .models import PaymentForm

from sre_constants import CATEGORY, CATEGORY_DIGIT
from sre_parse import CATEGORIES
from unicodedata import category
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.shortcuts import redirect, render
from users.models import User
from accounts.models import Transaction, Order, Order_item, Product, Customer, Checkout
from django.contrib.auth.models import auth
from django.contrib import messages
# Create your views here.

# M-Pesa Constants
MPESA_SHORTCODE = '174379'  # Replace with your Safaricom shortcode
MPESA_PASSKEY = 'MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMTYwMjE2MTY1NjI3'  # Replace with your passkey
MPESA_BASE_URL = 'https://sandbox.safaricom.co.ke'
CALLBACK_URL = 'https://03f2-41-89-227-171.ngrok-free.app/mpesa_callback/'




def home (request):
    product = Product.objects.all()
    context={}
    context["products"] = product
    

    return render(request,'index.html' ,context)
def register(request):
    if request.method == 'POST':
      
        Email= request.POST['email']
        
        password= request.POST.get('password')
        
        confirm= request.POST.get('confirm')
    
       # password = make_password(password)
        #confirm = make_password(confirm)
        
     
        if password == confirm:
           # password = make_password(password)
           password = make_password(password)
           user=User.objects.create(email=Email, password=password,is_active=True) 
           user.save()
           
        customer=Customer.objects.create(user=user)
        customer.save()
        
        return redirect('login')
    return render(request, 'signup.html')        


def login(request):
    if request.method == 'POST':
       email = request.POST.get('email')
       password = request.POST.get('password')
       user= auth.authenticate(request,email=email, password=password)
      
    #     user= User.objects.filter(email=email).first()

       if user is not None:
            auth.login(request,user)
            return redirect('/')  
       else:
            messages.error(request,'email or password incorrect') 
    
    return render(request,'login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('/')
    return render(request,'login.html')
   
def shipping(request):
    return render(request,'shipping.html')  

def save_data(request):
   
    # cart_total = order.get_cart_total()
  
   
    if request.method =='POST':
        Firstname=request.POST.get('Firstname')
        Lastname=request.POST.get('Lastname')
        payment=request.POST.get('AmountPaid')
      
        Checkout.objects.create( Firstname= Firstname, Lastname= Lastname,AmountPaid = payment)
    
    return redirect('/')
# def get_total(request):
#     if request.method == 'POST':
#         cart_total = order.get_cart_total()
#         return JsonResponse({'cart_total': cart_total}, safe=False)
#     return render(request, 'cart.html')
          
    


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
    
    user=Checkout.objects.create()
    return render(request, 'checkout.html',context)
    

def cart(request):
    context = {}
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        print(customer)
        cart_items = Order_item.objects.filter(order_id =order.id)
        # cart_items = order.orderitem_set.all()
        context['cart_items'] = cart_items
        context['order'] = order
    else:
        context['cart_items'] = []
        context['order'] = None
   
    return render(request, 'cart.html', context)
    
    # cart = request.session.get('cart', {})
    # cart_items = []
    # total = Decimal(0.00)

    # for item_id, item_data in cart.items():
    #     try:
    #         product = Product.objects.get(id=item_id)
    #         total += product.price * item_data['quantity']
    #         cart_items.append({
    #             'product': product,
    #             'quantity': item_data['quantity'],
    #             'total_price': product.price * item_data['quantity'],
    #         })
    #     except Product.DoesNotExist:
    #         pass

    # # Move context out of the loop
    # context = {
    #     'cart_items': cart_items,
    #     'total': total,
    # }

    # return render(request, 'cart.html', context)
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
    print('User......:',request.user)

    customer=request.user.customer  
    print("this--is the ====",customer)
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

def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Save the email to your database or perform any other action
        print(f"Subscribed with email: {email}")
        return JsonResponse({'message': 'Subscription successful!'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

    messages.add_message(request, messages.ERROR, 'A serious error occured !!!')
# M-Pesa Configuration
def generate_access_token():
    consumer_key='rGYP4yd8j4XCrnMe9trreUzM7aQe8XWYMpbBtEJjG8CGWsH0'
    consumer_secret='RXnUXwaG9knKSfuUqQPHNYa40SSxdaPdpOLPiUJSLmSj38YIewf5lH6qabCWaqA4'
    api_url='https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    
    response = requests.request("GET", 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials', headers = { 'Authorization': 'Basic ckdZUDR5ZDhqNFhDcm5NZTl0cnJlVXpNN2FRZThYV1lNcGJCdEVKakc4Q0dXc0gwOlJYblVYd2FHOWtuS1NmdVVxUVBITllhNDBTU3hkYVBkcE9MUGlVSlNMbVNqMzhZSWV3ZjVsSDZxYWJDV2FxQTQ=' })
    access_token = response.json().get('access_token')
    
    return access_token

def initiate_stk_push(phone, amount):
    try:
        token= generate_access_token()
        headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        stk_password = base64.b64encode(
            (MPESA_SHORTCODE + MPESA_PASSKEY + timestamp).encode()
        ).decode()
    except Exception as e:
        print(f"Failed to initiate STK Push: {str(e)}")
        return None
    
    
    try:
        request_body = {
             "BusinessShortCode": "174379",    
            "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMTYwMjE2MTY1NjI3",    
            "Timestamp":"20160216165627",    
            "TransactionType": "CustomerPayBillOnline",    
            "Amount": amount,    
            "PartyA":"254708374149",    
            "PartyB":"174379",    
            "PhoneNumber":phone,    
            "CallBackURL":CALLBACK_URL,    
            "AccountReference":"Test",    
            "TransactionDesc":"Test"
        }
       
        response = requests.post(
                f"{MPESA_BASE_URL}/mpesa/stkpush/v1/processrequest",
                json=request_body,
                headers=headers,
            ).json()
        return response
    except Exception as e:
        print(f"Failed to initiate STK Push: {str(e)}")
        return e
    
    
def format_phone_number(phone):
    phone = phone.replace("+", "")
    if re.match(r"^254\d{9}$", phone):
        return phone
    elif phone.startswith("0") and len(phone) == 10:
        return "254" + phone[1:]
    else:
        raise ValueError("Invalid phone number format")
def mpesa_callback_view(request):
    print("Received payment request", request)

    return HttpResponse("Payment request received successfully.",request.body)    

def mpesa_payment_view(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        #if form.is_valid():
        try:
            phone = request.POST["phone_number"]
            phone = format_phone_number(phone)
            
            amount = request.POST["amount"]
            response = initiate_stk_push(phone, amount)
            print(response)

            if response:
                checkout_request_id = response["CheckoutRequestID"]
                return render(request, "pending.html", {"checkout_request_id": checkout_request_id})
            else:
                error_message = response.get("errorMessage", "Failed to send STK push. Please try again.")
                return render(request, "mpesa_payment.html", {"form": form, "error_message": error_message})

        except ValueError as e:
            return render(request, "mpesa_payment.html", {"form": form, "error_message": str(e)})
        except Exception as e:
            return render(request, "mpesa_payment.html", {"form": form, "error_message": f"An unexpected error occurred: {str(e)}"})

    else:
        form = PaymentForm()

    return render(request, "mpesa_payment.html", {"form": form})
def payment_view(request):
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            try:
                phone = format_phone_number(form.cleaned_data["phone_number"])
                amount = form.cleaned_data["amount"]
                response = initiate_stk_push(phone, amount)
                print(response)

                if response:
                    print("we are......")
                    checkout_request_id = response["CheckoutRequestID"]
                    return render(request, "pending.html", {"checkout_request_id": checkout_request_id})
                else:
                    print("we are..errrr....")
                    error_message = response.get("errorMessage", "Failed to send STK push. Please try again.")
                    return render(request, "payment_form.html", {"form": form, "error_message": error_message})

            except ValueError as e:
                return render(request, "mpesa_payment.html", {"form": form, "error_message": str(e)})
            except Exception as e:
                return render(request, "mpesa_payment.html", {"form": form, "error_message": f"An unexpected error occurred: {str(e)}"})

    else:
        form = PaymentForm()

    return render(request, "mpesa_payment.html", {"form": form})

#def query_stk_push(checkout_request_id):
def query_stk_push():
    print("Quering...")
    try:
        token = generate_access_token()
        headers ={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(
            (MPESA_SHORTCODE + MPESA_PASSKEY + timestamp).encode()
        ).decode()
        request_body = {
            "BusinessShortCode": MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            #"CheckoutRequestID": checkout_request_id
             "TransactionType": "CustomerPayBillOnline",    
            "Amount": amount,    
            "PartyA":"254708374149",    
            "PartyB":"174379",    
            "PhoneNumber":phone,    
            "CallBackURL": CALLBACK_URL,    
            "AccountReference":"Test", 
               
            "TransactionDesc":"Test"
        }
        
        
        response = requests.post(   f"{MPESA_BASE_URL}/mpesa/stkpushquery/v1/query",
            json=request_body,
            headers=headers,
        )
        
        
        print(response.json())
        return response.json()

    except requests.RequestException as e:
        print(f"Error querying STK status: {str(e)}")
        return {"error": str(e)}
def stk_status_view(request):
    if request.method == 'POST':
        try:
            # Parse the JSON body
            data = json.loads(request.body)
            checkout_request_id = data.get('checkout_request_id')
            print("CheckoutRequestID:", checkout_request_id)

            # Query the STK push status using your backend function
            status = query_stk_push(checkout_request_id)

            # Return the status as a JSON response
            return JsonResponse({"status": status})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON body"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)
@csrf_exempt 
def payment_callback(request):
    print("Tuko kwa jtwara")
    # if request.method == "GET":
    #     print("Tuko kwa jtwara")
    #     #print(request.data)
    #     print(request.body)
        
    #     return HttpResponseBadRequest("Only POST requests are allowed")

    # try:
    #     # callback_data = json.loads(request.body)  # Parse the request body
    #     # result_code = callback_data["Body"]["stkCallback"]["ResultCode"]

    #     # if result_code == 0:
    #     #     # Successful transaction
    #     #     checkout_id = callback_data["Body"]["stkCallback"]["CheckoutRequestID"]
    #     #     metadata = callback_data["Body"]["stkCallback"]["CallbackMetadata"]["Item"]

    #     #     amount = next(item["Value"] for item in metadata if item["Name"] == "Amount")
    #     #     mpesa_code = next(item["Value"] for item in metadata if item["Name"] == "MpesaReceiptNumber")
    #     #     phone = next(item["Value"] for item in metadata if item["Name"] == "PhoneNumber")

    #     #     # Save transaction to the database
    #     #     Transaction.objects.create(
    #     #         amount=amount, 
    #     #         checkout_id=checkout_id, 
    #     #         mpesa_code=mpesa_code, 
    #     #         phone_number=phone, 
    #     #         status="Success"
    #     #     )
    #     #     return JsonResponse({"ResultCode": 0, "ResultDesc": "Payment successful"})

    #     # # Payment failed
    #     # return JsonResponse({"ResultCode": result_code, "ResultDesc": "Payment failed"})

    # except (json.JSONDecodeError, KeyError) as e:
    #     return HttpResponseBadRequest(f"Invalid request data: {str(e)}")
#     try:
#         credentials = f"{CONSUMER_KEY}:{CONSUMER_SECRET}"
#         encoded_credentials = base64.b64encode(credentials.encode()).decode()

#         headers = {
#             "Authorization": f"Basic {encoded_credentials}",
#             "Content-Type": "application/json",
#         }
#         response = requests.get(
#             f"{MPESA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials",
#             headers=headers,
#         ).json()

#         if "access_token" in response:
#             return response["access_token"]
#         else:
#             raise Exception("Access token missing in response.")

#     except requests.RequestException as e:
#         raise Exception(f"Failed to connect to M-Pesa: {str(e)}")
    
#     def initiate_stk_push(phone, amount):
#         try:
#             token = generate_access_token()
#             headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
#             timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
#             stk_password = base64.b64encode(
#                 (MPESA_SHORTCODE + MPESA_PASSKEY + timestamp).encode()
#             ).decode()

#             request_body = {
#                 "BusinessShortCode": MPESA_SHORTCODE,
#                 "Password": stk_password,
#                 "Timestamp": timestamp,
#                 "TransactionType": "CustomerPayBillOnline",
#                 "Amount": amount,
#                 "PartyA": phone,
#                 "PartyB": MPESA_SHORTCODE,
#                 "PhoneNumber": phone,
#                 "CallBackURL": CALLBACK_URL,
#                 "AccountReference": "account",
#                 "TransactionDesc": "Payment for goods",
#             }

#             response = requests.post(
#                 f"{MPESA_BASE_URL}/mpesa/stkpush/v1/processrequest",
#                 json=request_body,
#                 headers=headers,
#             ).json()

#             return response

#         except Exception as e:
#             print(f"Failed to initiate STK Push: {str(e)}")
#             return e
        
# def payment_view(request):
#         if request.method == "POST":
#             form = PaymentForm(request.POST)
#             if form.is_valid():
#                 try:
#                     phone = format_phone_number(form.cleaned_data["phone_number"])
#                     amount = form.cleaned_data["amount"]
#                     response = initiate_stk_push(phone, amount)
#                     print(response)
    
#                     if response.get("ResponseCode") == "0":
#                         checkout_request_id = response["CheckoutRequestID"]
#                         return render(request, "pending.html", {"checkout_request_id": checkout_request_id})
#                     else:
#                         error_message = response.get("errorMessage", "Failed to send STK push. Please try again.")
#                         return render(request, "payment_form.html", {"form": form, "error_message": error_message})
    
#                 except ValueError as e:
#                     return render(request, "payment_form.html", {"form": form, "error_message": str(e)})
#                 except Exception as e:
#                     return render(request, "payment_form.html", {"form": form, "error_message": f"An unexpected error occurred: {str(e)}"})
    
#         else:
#             form = PaymentForm()
    
#         return render(request, "payment_form.html", {"form": form})

# def query_stk_push(checkout_request_id):
#     print("Quering...")
#     try:
#         token = generate_access_token()
#         headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

#         timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
#         password = base64.b64encode(
#             (MPESA_SHORTCODE + MPESA_PASSKEY + timestamp).encode()
#         ).decode()

#         request_body = {
#             "BusinessShortCode": MPESA_SHORTCODE,
#             "Password": password,
#             "Timestamp": timestamp,
#             "CheckoutRequestID": checkout_request_id
#         }

#         response = requests.post(
#             f"{MPESA_BASE_URL}/mpesa/stkpushquery/v1/query",
#             json=request_body,
#             headers=headers,
#         )
#         print(response.json())
#         return response.json()

#     except requests.RequestException as e:
#         print(f"Error querying STK status: {str(e)}")
#         return {"error": str(e)}
# def stk_status_view(request):
#     if request.method == 'POST':
#         try:
#             # Parse the JSON body
#             data = json.loads(request.body)
#             checkout_request_id = data.get('checkout_request_id')
#             print("CheckoutRequestID:", checkout_request_id)

#             # Query the STK push status using your backend function
#             status = query_stk_push(checkout_request_id)

#             # Return the status as a JSON response
#             return JsonResponse({"status": status})
#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON body"}, status=400)

#     return JsonResponse({"error": "Invalid request method"}, status=405)
# @csrf_exempt  # To allow POST requests from external sources like M-Pesa


# def payment_callback(request):
#     if request.method != "POST":
#         return HttpResponseBadRequest("Only POST requests are allowed")

#     try:
#         callback_data = json.loads(request.body)  # Parse the request body
#         result_code = callback_data["Body"]["stkCallback"]["ResultCode"]

#         if result_code == 0:
#             # Successful transaction
#             checkout_id = callback_data["Body"]["stkCallback"]["CheckoutRequestID"]
#             metadata = callback_data["Body"]["stkCallback"]["CallbackMetadata"]["Item"]

#             amount = next(item["Value"] for item in metadata if item["Name"] == "Amount")
#             mpesa_code = next(item["Value"] for item in metadata if item["Name"] == "MpesaReceiptNumber")
#             phone = next(item["Value"] for item in metadata if item["Name"] == "PhoneNumber")

#             # Save transaction to the database
#             Transaction.objects.create(
#                 amount=amount, 
#                 checkout_id=checkout_id, 
#                 mpesa_code=mpesa_code, 
#                 phone_number=phone, 
#                 status="Success"
#             )
#             return JsonResponse({"ResultCode": 0, "ResultDesc": "Payment successful"})

#         # Payment failed
#         return JsonResponse({"ResultCode": result_code, "ResultDesc": "Payment failed"})

#     except (json.JSONDecodeError, KeyError) as e:
#         return HttpResponseBadRequest(f"Invalid request data: {str(e)}")

# def format_phone_number(phone):
#     phone = phone.replace("+", "")
#     if re.match(r"^254\d{9}$", phone):
#         return phone
#     elif phone.startswith("0") and len(phone) == 10:
#         return "254" + phone[1:]
#     else:
#         raise ValueError("Invalid phone number format")
