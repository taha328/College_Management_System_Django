from django.contrib import admin
from .models import  DossierEtudiant, Stage,  Resultat, InscriptionPédagogique, Matiere, Professeur,  Cycle
from django.contrib import admin
from .models import DossierEtudiant
from .forms import DossierEtudiantCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect

class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)

@admin.register(DossierEtudiant)
class DossierEtudiantAdmin(admin.ModelAdmin):
    list_display = ('Cne', 'nom', 'prenom', 'Cne', 'sexe', 'numero_tele', 'ville', 'email', 'Dernier_diplome_obtenu', 'adresse', 'Formation_souhaitée', 'note_s1', 'note_s2', 'note_s3', 'note_s4', 'note_s5', 'note_s6', 'display_transcript_link')

    def display_transcript_link(self, obj):
        return f'<a href="{obj.get_transcript_download_url()}" download>Download</a>' if obj.get_transcript_download_url() else '-'

    display_transcript_link.allow_tags = True
    display_transcript_link.short_description = 'Transcript Download'

    actions = ['create_users_for_selected']

    def create_users_for_selected(self, request, queryset):
        # Redirect to the user creation form with the necessary parameters
        cne_list = ','.join(str(dossier.Cne) for dossier in queryset)
        url = reverse('admin:auth_user_add') + f'?username={cne_list}&password_creation=True'
        return HttpResponseRedirect(url)

    create_users_for_selected.short_description = "Create user accounts for selected Dossier Etudiants"

    def add_view(self, request, form_url='', extra_context=None):
        # Override add_view to pre-fill the username and handle password creation
        if request.GET.get('password_creation') == 'True':
            username = request.GET.get('username')
            extra_context = extra_context or {}
            extra_context['username'] = username
            extra_context['show_password_form'] = True

        return super().add_view(request, form_url=form_url, extra_context=extra_context)
    
class InscriptionPédagogiqueForm(forms.ModelForm):
    class Meta:
        model = InscriptionPédagogique
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit the choices for the 'etudiant' field to non-staff users
        self.fields['user'].queryset = User.objects.filter(is_staff=False)

class InscriptionPédagogiqueAdmin(admin.ModelAdmin):
    form = InscriptionPédagogiqueForm
class ResultatForm(forms.ModelForm):
    class Meta:
        model = Resultat
        exclude = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit the choices for the 'etudiant' field to non-staff users
        self.fields['etudiant'].queryset = User.objects.filter(is_staff=False)

class ResultatAdmin(admin.ModelAdmin):
    form = ResultatForm
admin.site.register(Stage)
admin.site.register(Resultat, ResultatAdmin)
admin.site.register(InscriptionPédagogique, InscriptionPédagogiqueAdmin)
admin.site.register(Matiere)
admin.site.register(Professeur)
admin.site.register(Cycle)
