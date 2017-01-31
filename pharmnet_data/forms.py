from django import forms
from django.core.exceptions import ValidationError


class UploadFileForm(forms.Form):
    entete_achats_file = forms.FileField(label="Entete des Achats",
                               widget=forms.FileInput(attrs={'class': 'form-control','required':'true'}))
    details_achats_file = forms.FileField(label="Lignes des Achats", max_length=30,
                               widget=forms.FileInput(attrs={'class': 'form-control','required':'true'}))

    def clean_entete_achats_file(self):
        file = self.cleaned_data['entete_achats_file'].name
        if file != 'IEACH00.DBF':
            raise ValidationError('Fichier incorrect, vous devez choisir IEACH00.DBF')
        else:
            return True
    def clean_details_achats_file(self):
        file = self.cleaned_data['details_achats_file'].name
        if file != 'ILACH00.DBF':
            raise ValidationError('Fichier incorrect, vous devez choisir ILACH00.DBF')
        else:
            return True
