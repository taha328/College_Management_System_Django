import os
import environ
import sys
from pathlib import Path

# Disable creation of .pyc files and __pycache__ directories
sys.dont_write_bytecode = True

# Initialize environment variables manager
env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY SETTINGS
# Fetch secret key from environment variable; fallback to a default value in development
SECRET_KEY = env('DJANGO_SECRET_KEY', default='django-insecure-default-secret-key')

# DEBUG mode; set to False in production
DEBUG = True

# Allowed hosts; update with actual domain names in production
ALLOWED_HOSTS = ['*']

# SECURE PROXY SETTINGS
# Configure secure proxy SSL header
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# CSRF AND CORS SETTINGS
# Define trusted origins for CSRF and CORS
CSRF_TRUSTED_ORIGINS = [
    "https://apogee.twc1.net",
    "http://0.0.0.0:8000",
    # Add additional trusted origins as needed
]
CORS_ALLOWED_ORIGINS = [
    "https://apogee.twc1.net",
    "http://0.0.0.0:8000",
    # Add additional allowed origins as needed
]
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Add your template directories if any
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',  # Add this for static files in templates
            ],
        },
    },
]

# APPLICATIONS SETTINGS
INSTALLED_APPS = [
    "admin_interface",
    "colorfield",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apogee_',
]

# MIDDLEWARE SETTINGS
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',

]

# STATIC FILES SETTINGS
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# DATABASE SETTINGS
# Fetch database configurations from environment variables
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': 'db',
        'PORT': '5432',
    }
}

# INTERNATIONALIZATION AND LOCALIZATION SETTINGS
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# MEDIA SETTINGS
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# DEFAULT AUTO FIELD SETTINGS
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# AUTHENTICATION SETTINGS
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# URL Configuration
ROOT_URLCONF = 'apogee.urls'

# WSGI Application
WSGI_APPLICATION = 'apogee.wsgi.application'

# Authentication URLs
LOGIN_URL = '/login/'  # Adjust the URL as needed
LOGOUT_URL = 'logout'
