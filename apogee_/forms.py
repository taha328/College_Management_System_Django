# college_app/forms.py
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import  DossierEtudiant, Stage, ControleConnaissances, Resultat, InscriptionPédagogique

class DossierEtudiantForm(forms.ModelForm):
    class Meta:
        model = DossierEtudiant
        fields = '__all__'
        transcript = forms.FileField(label='Transcript (PDF)', required=False, widget=forms.FileInput(attrs={'accept': 'application/pdf'}))
class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = '__all__'

class ControleConnaissancesForm(forms.ModelForm):
    class Meta:
        model = ControleConnaissances
        fields = '__all__'

class ResultatForm(forms.ModelForm):
    class Meta:
        model = Resultat
        fields = '__all__'

class InscriptionPédagogiqueForm(forms.ModelForm):
    class Meta:
        model = InscriptionPédagogique
        fields = '__all__'
class DossierEtudiantCreationForm(UserCreationForm):
    cne = forms.ModelChoiceField(queryset=DossierEtudiant.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'vForeignKeyRawIdAdminField'}))

    class Meta:
        model = User
        fields = ('cne', 'password1', 'password2')

    def save(self, commit=True):
        dossier_etudiant = self.cleaned_data['cne']
        user = super(DossierEtudiantCreationForm, self).save(commit=False)

        # Set the first name, last name, and email based on DossierEtudiant
        user.first_name = dossier_etudiant.nom  # Replace 'nom' with the actual field name
        user.last_name = dossier_etudiant.prenom  # Replace 'prenom' with the actual field name
        user.email = dossier_etudiant.email  # Replace 'email' with the actual field name

        # Set the username based on Cne
        user.username = str(dossier_etudiant.Cne)

        if commit:
            user.save()
        return user
