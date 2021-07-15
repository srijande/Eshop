from django.contrib import auth
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
import json
import datetime
from .models import * 
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import HttpResponseRedirect
# from .utils import cookieCart, cartData, guestOrder
def store(request):
     if request.user.is_authenticated:
          customer=request.user
          order, created = Order.objects.get_or_create(customer=customer,complete=False)
          items=order.orderitem_set.all()
          cartItems=order.get_cart_items
     else:
          try:
               cart=json.loads(request.COOKIES['cart'])
          except:
               cart={}

          items = [] 
          order={'get_cart_total':0,'get_cart_items':0}
          cartItems=order['get_cart_items'] 
          for i in cart:
               cartItems+=cart[i]['quantity']
    
               

     products=Product.objects.all()
     context = {'products':products,'cartitems':cartItems}
     return render(request, 'store/store.html', context)
     

def cart(request):
     if request.user.is_authenticated:
          customer=request.user
          order, created = Order.objects.get_or_create(customer=customer,complete=False)
          items=order.orderitem_set.all()
          cartItems=order.get_cart_items
     else:
          try:
               cart=json.loads(request.COOKIES['cart'])
          except:
               cart={}

          items = [] 
          order={'get_cart_total':0,'get_cart_items':0}
          cartItems=order['get_cart_items'] 
          for i in cart:
               cartItems+=cart[i]['quantity']
     
     context = {'items': items,'order':order,'cartitems':cartItems}
     return render(request, 'store/cart.html', context)

def checkout(request):
       if request.user.is_authenticated:
          customer=request.user
          order, created = Order.objects.get_or_create(customer=customer,complete=False)
          items=order.orderitem_set.all()
          cartItems=order.get_cart_items
       else:
          items = []
     
       context = {'items': items,'order':order,'cartitems':cartItems,}
       return render(request, 'store/checkout.html', context)


def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)
	customer = request.user
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)


def loginpage(request):
     if request.method == 'POST':
         username= request.POST.get('username')
         password= request.POST.get('password')
         user = authenticate(request,username=username, password= password)
         if user is not None:
          login(request,user)
          return redirect('store')
     return render(request,'store/login.html',{})
     
def processOrder(request):
     transaction_id = datetime.datetime.now().timestamp()
     data = json.loads(request.body)
     if request.user.is_authenticated:
	        customer = request.user
	        order, created = Order.objects.get_or_create(customer=customer, complete=False)
     
		    
     total = float(data['form']['total'])
     order.transaction_id = transaction_id
     if total == order.get_cart_total:
		                             order.complete = True
     order.save()
     ShippingAddress.objects.create(
		customer=customer,
		order=order,
          address=data['shipping']['address'],
		city=data['shipping']['city'],
          state=data['shipping']['state'],
		pincode=data['shipping']['pincode'],
		)
          
     return JsonResponse('Payment Submitted',safe=False)

def register(request):
     form = CreateUserForm() 
     if request.method == 'POST':
          form = CreateUserForm(request.POST)
          if form.is_valid():
                form.save()
                user=form.cleaned_data.get('username')
                messages.success(request,'Account successfully created'+user)
                return redirect('login')


          else :
                print('aaste')
     context = {'form':form}
     return render(request,'store/register.html',context)


def logout_view(request):
     logout(request)
     return redirect('store')