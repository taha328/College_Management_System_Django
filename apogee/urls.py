from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
 
    path('admin/', admin.site.urls),
    path('', include('apogee_.urls')),


     #new
]
admin.site.site_header = "FST TANGER ADMINISTRATION"