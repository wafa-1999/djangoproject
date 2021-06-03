from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Produit(models.Model):
    TYPE_CHOICES = [('fr', 'Frais'), ('cs', 'Conserve'), ('em', 'emballe')]
    libelle = models.CharField(max_length=100)
    description = models.TextField(default='Non definie')
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default='em')
    prix = models.DecimalField(max_digits=10, decimal_places=3, default=0.000)
    img = models.ImageField(blank=True, default='aliment.jpg')
    digital = models.BooleanField(default=False,null=True, blank=True)
    

    Fournisseur = models.ForeignKey(
        'Fournisseur', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.libelle+" "+self.description+" "+str(self.prix)
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Emballage(models.Model):
    COUL_CHOICES = [('bl', 'blanc'), ('rg', 'rouge'),
                     ('ble', 'bleur'), ('vr', 'vert'), ('multi', 'multicolore')]
    matiere = models.CharField(max_length=100)
    couleur = models.CharField(
        max_length=10, default='transparent', choices=COUL_CHOICES)

    def __str__(self):
        return self.matiere+" "+self.couleur


class Fournisseur(models.Model):
    nom = models.CharField(max_length=100)
    adresse = models.TextField()
    email = models.EmailField()
    img = models.ImageField(blank=True, default='aliment.jpg')

    def __str__(self):
        return self.nom+" "+self.adresse+" "+self.email+" "


class ProduitC(Produit):
    Duree_garantie = models.CharField(max_length=100)

    def __str__(self):
        return self.Duree_garantie


class Commande(models.Model):
    Duree_garantie = models.CharField(max_length=100)
    dateCde = models.DateField(null=True, default=date.today)
    totalCde = models.DecimalField(max_digits=10, decimal_places=3)
    Produits = models.ManyToManyField('Produit')

    def __dtr__(self):
        return self.Duree_garantie+" "+self.dateCde+" "+self.totalCde


class Limited(models.Model):
    TYPE_CHOICES = [('fr', 'Frais'), ('cs', 'Conserve'), ('em', 'emballe')]
    libelle = models.CharField(max_length=100)
    description = models.TextField(default='Non definie')
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default='em')
    prix = models.DecimalField(max_digits=10, decimal_places=3, default=0.000)
    image = models.ImageField(blank=True, default='aliment.jpg')

    def __str__(self):
        return self.libelle+" "+self.description+" "+str(self.prix)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.produit.digital == False:
                shipping = True
        return shipping
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total 
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total 


class OrderItem(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.produit.prix * self.quantity
        return total


class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return self.adresse
