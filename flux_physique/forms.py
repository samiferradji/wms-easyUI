# -*- coding: utf-8 -*-
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm, TextInput, Select
from refereces.models import Magasin, DepuisMagasinsAutorise, VersMagasinsAutorise
from flux_physique.models import Transfert, Stock, DetailsTransfert, Produit, StatutDocument
from django import forms


class TransfertModelForm(ModelForm):

    class Meta:
        default_statut_doc = StatutDocument.objects.order_by('id').first()
        model = Transfert
        fields = ('depuis_magasin','vers_magasin','statut_doc','created_by')
        widgets = {
            'depuis_magasin': Select(attrs={'id': 'depuis_magasin_select'}),
            'vers_magasin': Select(attrs={'id': 'vers_magasin_select'}),
            'statut_doc': TextInput(attrs={'id': 'statut_doc', 'value': default_statut_doc}),
        }
    def __init__(self, user=None, **kwargs):
        super(TransfertModelForm, self).__init__(**kwargs)
        if user:
            self.fields['depuis_magasin'].queryset = Magasin.objects.filter(depuismagasinsautorise__user=user)
            self.fields['vers_magasin'].queryset = Magasin.objects.filter(versmagasinsautorise__user=user)


class ProductModelForm(ModelForm):
    class Meta:
        model = Stock
        fields = ('produit',)
        widgets = {
            'produit': Select(attrs={'id': 'select_product'}),
        }

    def __init__(self, user=None, **kwargs):
        super(ProductModelForm, self).__init__(**kwargs)
        produit_in_Stock = Stock.objects.values_list('produit__id').distinct()
        self.fields['produit'].queryset = Produit.objects.filter(id__in=produit_in_Stock).order_by('produit')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))


class EntreposageModelForm(ModelForm):

    class Meta:
        default_statut_doc = StatutDocument.objects.order_by('id').first()
        model = Transfert
        fields = ('depuis_magasin','statut_doc','created_by')
        widgets = {
            'depuis_magasin': Select(attrs={'id': 'depuis_magasin_select'}),
            'statut_doc': TextInput(attrs={'id': 'statut_doc', 'value': default_statut_doc}),
        }
        labels = {'depuis_magasin':'Magasin'}

    def __init__(self, user=None, **kwargs):
        super(EntreposageModelForm, self).__init__(**kwargs)
        if user:
            self.fields['depuis_magasin'].queryset = Magasin.objects.filter(depuismagasinsautorise__user=user)
