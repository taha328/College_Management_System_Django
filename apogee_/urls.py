# apogee_/urls.py
from django.urls import path
from .views import LoginView, LogoutView, interface_etudiant, enter_student_info, student_home, homepage, download_convocation, generate_student_report
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', homepage, name='homepage'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('resultats/', interface_etudiant, name='resultats'),
    path('enter_student_info/', enter_student_info, name='enter_student_info'),
    path('student_home/', student_home, name='student_home'),
    path('download_convocation/', download_convocation, name='download_convocation'),
    path('generate_student_report/', generate_student_report, name='generate_student_report'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

