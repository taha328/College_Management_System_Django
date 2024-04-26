# accounts/views.py
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Resultat,  Stage,  InscriptionPédagogique, User
from django.db.models import Sum
from .forms import DossierEtudiantForm
from django.urls import reverse
from django.template.loader import get_template
from xhtml2pdf import pisa
from decimal import Decimal
from django.shortcuts import render

def homepage(request):
    return render(request, 'apogee_/homepage.html')

class LoginView(BaseLoginView):
    template_name = 'apogee_/login.html'
    authentication_form = AuthenticationForm

    def get_success_url(self):
        # Replace 'interface_etudiant' with the actual name or URL pattern of the student home page
        return reverse('student_home')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_staff:
            # Redirect staff members to a different page (e.g., permission denied)
            return redirect('admin:index')
        
        return super().dispatch(request, *args, **kwargs)

class LogoutView(BaseLogoutView):
    # Redirect to the login page after logout
    next_page = 'login'

@login_required
def interface_etudiant(request):
    user = request.user
    results = Resultat.objects.filter(etudiant=user)

    if results.exists():
        # Calculate the average grade
        moyenne_generale = results.aggregate(Sum('moyennes'))['moyennes__sum'] / results.count()
        # Round to two decimal places
        moyenne_generale = round(moyenne_generale, 2)
    else:
        moyenne_generale = Decimal('0.00')  # Set a default value if there are no results

    context = {'results': results, 'moyenne_generale': moyenne_generale}
    return render(request, 'apogee_/resultats.html', context)

def enter_student_info(request):
    if request.method == 'POST':
        form = DossierEtudiantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to a success page
    else:
        form = DossierEtudiantForm()

    return render(request, 'apogee_/infos_etudiant.html', {'form': form})

@login_required
def student_home(request):
    # You can add any context data you want to pass to the template
    context = {
        'user': request.user  # You might want to pass other user-related data
    }

    return render(request, 'apogee_/student_home.html', context)
@login_required
def download_convocation(request):
    # Get user information and other data needed for the convocation
    print(f"User: {request.user}, Staff: {request.user.is_staff}")
    if request.user.is_staff:
        return HttpResponse('Error: Staff users are not allowed to download convocations.')    
    user = request.user
    user_first_name = user.first_name
    user_last_name = user.last_name
    user_email = user.email

    # Retrieve the associated DossierEtudiant instance
        # Get the latest Stage instance for the current user
    try:
        stage = Stage.objects.filter(user=user).latest('id')
    except Stage.DoesNotExist:
        # Handle the case where no Stage object is found
        return HttpResponse('Error: Stage object not found for this user.')

    # Get the associated InscriptionPédagogique instance
    inscription = InscriptionPédagogique.objects.filter(user=user).latest('id')

    # Render the convocation as HTML
    template_path = 'apogee_/convocation_template.html'
    context = {
        'user': user,
        'stage': stage,
        'email': user_email,
        'nom': user_first_name,
        'prenom': user_last_name,
        'cycle': inscription.cycle,
        'entreprise': stage.entreprise,
        'adresse': stage.adresse_d_entreprise,
        'periode_de_stage': stage.periode_de_stage,
        'convocation':stage.convention_stage,
    }


    template = get_template(template_path)
    html_content = template.render(context)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="convocation.pdf"'

    # Generate PDF
    pisa_status = pisa.CreatePDF(html_content, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF')

    return response

@login_required
def convocation_template(request):
    # Get the latest Stage instance for the current user
    stage = Stage.objects.filter(user=user).latest('id')  # Assuming you have an 'id' field for ordering
    user = request.user
    user_first_name = user.first_name
    user_last_name = user.last_name
    user_email = user.email
    # Get the associated InscriptionPédagogique instance
    inscription = InscriptionPédagogique.objects.filter(etudiant__user=request.user).latest('id')

    context = {
        'user': user,
        'stage': stage,
        'email': user_email,
        'nom': user_first_name,
        'prenom': user_last_name,
        'cycle': inscription.cycle,
        'entreprise': stage.entreprise,
        'adresse': stage.adresse_d_entreprise,
        'periode_de_stage': stage.periode_de_stage,
    }


    return render(request, 'apogee_/convocation_template.html', context)

@login_required
def generate_student_report(request):
    # Get the logged-in user
    user = request.user
    user_first_name = user.first_name
    user_last_name = user.last_name
    user_email = user.email

    resultats = Resultat.objects.filter(etudiant=user)

    # Render the PDF content
    inscription = InscriptionPédagogique.objects.filter(user=user).latest('id')
    template_path = 'apogee_/report_template.html'  # Update with the actual path
    context = {'etudiant': user,'nom': user_first_name,'prenom': user_last_name,'email': user_email,'cycle': inscription.cycle, 'resultats': resultats,}
    template = get_template(template_path)
    html_content = template.render(context)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="student_report.pdf"'

    # Generate PDF
    pisa_status = pisa.CreatePDF(html_content, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF')

    return response