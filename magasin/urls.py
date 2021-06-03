from django.urls import path,include
from django.conf.urls import url
from . import views


urlpatterns = [
    
    path('Produit/',views.index5),
    #path('Commande/',views.mesCommandes),
    path('Fournisseur/',views.index3),
    #path('Products/',views.index4),
    path('LimitedEdition/',views.index6),
    path('contact/', views.contactView),
    path('success/', views.successView),
     
    path('store/',views.store),
    path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),

	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
]
