from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from .models import * 
from .forms import ProduitForm,CommandeForm,ContactForm
from django.shortcuts import redirect
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder

# Create your views here.

def index(request):
    list=Produit.objects.all() 
    return render(request,'magasin/vitrine.html',{'list':list})
 

def index2(request): 
    if request.method == "POST" : 
        form = ProduitForm(request.POST,request.FILES) 
        if form.is_valid(): 
            form.save() 
            return redirect('/magasin')
    else : 
        form = ProduitForm() 
    return render(request,'magasin/majProduits.html',{'form':form})
def index3(request):
    fournisseurs=Fournisseur.objects.all() 
    ctx= {'fournisseurs':fournisseurs}
    return render(request,'magasin/fournisseur.html',ctx)
#def index3(request):
 #   if request.method == "POST" :
  #      form = CommandeForm(request.POST,request.FILES) 
   #     if form.is_valid(): 
    #        form.save() 
     #       return redirect('/magasin') 
   # else :             
    #    form = CommandeForm() 
    #return render(request,'magasin/majCommande.html',{'form':form})
def index4(request):
    list=Produit.objects.all() 
    return render(request,'magasin/products.html',{'list':list})
def index5(request):
    limiteds=Limited.objects.all() 
    ctx= {'limiteds':limiteds}
    return render(request,'magasin/vitrine.html',ctx)
def index6(request):
    limiteds=Limited.objects.all() 
    ctx= {'limiteds':limiteds}
    return render(request,'magasin/LimitedEdition.html',ctx)
def order(request):
    ctx = {'active_link': 'order'}
    return render(request, 'magasin/order.html',ctx)

def contactView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['foufabarkallah1999@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "magasin/email.html", {'form': form})
 
def successView(request):
    return HttpResponse('Success! Thank you for your message.')






def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    products = Produit.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'magasin/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'magasin/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'magasin/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	produitId = data['produitId']
	action = data['action']
	print('Action:', action)
	print('produit:', produitId)

	customer = request.user.customer
	produit = Produit.objects.get(id=produitId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, produit=produit)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)