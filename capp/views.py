import datetime
import json
from urllib import response
from django.shortcuts import render,redirect
from django.shortcuts import HttpResponseRedirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login as django_login
from .forms import RegistrationForm,ProductForm
from .models import product as product2,order

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import razorpay

from django.shortcuts import render
# import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

razorpay_client = razorpay.Client(
    auth=('rzp_test_yke62IssIzsbxu', 'MmRX9hMcVlGLp2NmmKC2fdWS'))

# Create your views here.

def login(request):
  if request.method=="GET":
    context={}
    context['form']=AuthenticationForm()
    context['registration']=RegistrationForm()
    return render(request,'login.html',context)
  elif request.method=="POST":
    form=AuthenticationForm(data=request.POST)
    if form.is_valid():
      username=form.cleaned_data.get('username')
      password=form.cleaned_data.get('password')
      user=authenticate(request,username=username,password=password)
      if user:
        django_login(request=request,user=user)
        if request.user.is_superuser:
          return redirect('admin-index')
        else:
          return redirect('home')
      else:
        context={}
        context['form']=form
        return render(request,'login.html',context)
    else:
        context={}
        context['form']=form
        return render(request,'login.html',context)
def signup(request):
    if request.method == 'POST':
        f = RegistrationForm(request.POST)
        if f.is_valid():
            f.save()
            return redirect('login')
        context={}
        context['form']=AuthenticationForm()
        context['registration']=f
        return render(request,'login.html',context)
    else:
        context={}
        context['form']=AuthenticationForm()
        context['registration']=RegistrationForm()

    return render(request,'login.html',context)

def home(request):
    return render(request,'home.html')
  
def adminIndex(request):
  if request.method=="GET":
    context={}
    context['form']=ProductForm()
    return render(request,'admin_index.html',context)
  elif request.method=="POST":
    form=ProductForm(request.POST,request.FILES)
    if form.is_valid():
      form.save()
    else:
        context={}
        context['form']=form
        return render(request,'admin_index.html',context)
    return render(request,'admin_index.html')
  


def product(request,pid):
  print("Hello World")
  product=product2.objects.get(product_id=pid)
  product_val={
    'product':product2.objects.get(product_id=pid),
    'rproduct':product2.objects.filter(category=product.category).all().order_by('id')
  }
  return render(request,'product.html',product_val)
  
  
def productpage(request):
  print(request.GET,"ppppp")
  name=request.GET.get('q',None)
  if name:
    product_val={
        'product':product2.objects.filter(product_name__contains=name).all(),
    }
       
  else:
    product_val={
        'product':product2.objects.all(),
      
        
    }
  return render(request,'productpage.html',product_val) 

def cart(request):
  products=product2.objects.all()
  return render(request,'cart.html',{'products':products})

def account(request):
  products=product2.objects.all()
  orders = order.objects.filter(status='1').filter(user_name=request.user)
  return render(request,'account.html',{'orders':orders,'products':products})
  return HttpResponse(request.user)

def checkout(request):
  products=product2.objects.all()
  return render(request,'checkout.html',{'products':products})

def generateOrder(request):
  if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        country = request.POST['country']
        address = request.POST['address']
        email = request.POST['email']
        phone = request.POST['phone']
        product_items = request.POST['product_items']
        user_name = request.POST['user_name']
        total = request.POST['total']
        date = datetime.date.today()
        orders=order.objects.create(first_name=first_name,email=email,last_name=last_name,country=country,address=address,products=product_items,user_name=user_name,date=date,status='0',total_amount=total,phone=phone)
        name = first_name+" "+last_name
        # generates razorpay
        client = razorpay.Client(auth=("rzp_test_yke62IssIzsbxu", "MmRX9hMcVlGLp2NmmKC2fdWS"))
        payment = client.order.create({'amount':  int(total) * 100, 'currency': 'INR','payment_capture': '1'})
        # insert payment id to order table
        orders.provider_order_id = payment['id']
        orders.save()
  return render(request, 'payment.html',{'payment_id':payment['id'],'order_id':orders.id,'name':name,'email':email,'phone':phone,'address':address,'total':total})

@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=("rzp_test_yke62IssIzsbxu", "MmRX9hMcVlGLp2NmmKC2fdWS"))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        orders = order.objects.get(provider_order_id=provider_order_id)
        orders.payment_id = payment_id
        orders.provider_order_id = provider_order_id
        orders.signature_id = signature_id
        orders.status = '1'
        orders.save()
        return render(request,'payment_success.html')
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get("order_id")
        orders = order.objects.get(provider_order_id=provider_order_id)
        orders.payment_id = payment_id
        orders.provider_order_id = provider_order_id
        orders.save()
        return render(request,'payment_error.html')
      
def clearCart(request):
  return render(request,'clear_cart.html',{'user':request.user})

def orders(request):
  orders = order.objects.filter(status='1').filter(user_name=request.user)
  return render(request,'orders.html',{'orders':orders})

def success(request):
  return render(request,'payment_success.html')