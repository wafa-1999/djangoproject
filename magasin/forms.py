from django.forms import ModelForm 
from .models import Produit,Commande
from django import forms

class ProduitForm(ModelForm): 
    class Meta :
        model = Produit 
        fields = "__all__" #pour tous les champs de la table
class CommandeForm(ModelForm):
    class Meta :
        model = Commande
        fields = "__all__"

class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)