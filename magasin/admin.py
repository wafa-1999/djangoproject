from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Produit)
admin.site.register(Fournisseur)
admin.site.register(Commande)
admin.site.register(Limited)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

