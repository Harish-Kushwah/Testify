
from pathlib import Path
import os
import dj_database_url
import cloudinary
import cloudinary.uploader
import cloudinary.api

BASE_DIR = Path(__file__).resolve().parent.parent

#===================[DEVELOPMENT SECTION]=================================
# DEBUG =True
# ALLOWED_HOSTS = []

# STATICFILES_DIRS =[
#     os.path.join(BASE_DIR,'Test/static')
# ]
#STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# SECRET_ROOT = os.path.join(BASE_DIR,'')

# for media files
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR,'media')

#Default database for development purpose
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

#NOTE:CURRENTLY USING LOCAL OFFLINE DATABASE POSTGREES NEED TO CHANGE WHILE DEPLOYMENT
#NOTE:MEDIA FILE STORING IN cloudinary
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
cloudinary.config( 
   cloud_name = "dfdvv1awl",
    api_key = "828992967288959",
    api_secret ="O10H2zW0KtVg-wp3UG-7m5cjYaw"
) 
#=======================================================================

#===================[DEPLOYMENT SECTION]=================================
# Environment variables set ---------------------------------------------

SECRET_KEY = os.environ.get("SECRET_KEY")
DEBUG = os.environ.get('DEBUG' , 'FALSE').lower == "true"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(" ")


#cloudinary is image hosting service provider used for serving media files---


# cloudinary configuration for using cloudinary
cloudinary.config( 
    cloud_name =os.environ.get("CLOUD_NAME"),
    api_key = os.environ.get("API_KEY"),
    api_secret =os.environ.get("API_SECRET")
) 

#using cloudinary storage for media files storage
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.RawMediaCloudinaryStorage'
MEDIA_URL = '/OnlineMockTest/media/'
MEDIA_ROOT = BASE_DIR / 'media'

#[serving static files]--------------------------------------------------------
STATIC_URL ='/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"


#[for deploying database] -------------------------------------------------------

database_url = os.environ.get("DATABASE_URL")
DATABASES['default'] = dj_database_url.parse(database_url)
# =============================================================================



# =========================[OTHER SETTINGS]=========================================
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
# Application definition

INSTALLED_APPS = [
    'Test',
    'whitenoise.runserver_nostatic', #added for serving static files in development
    'cloudinary_storage',            #added for serving media files in development
    'cloudinary',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",  #required middleware for serving static files in development
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'OnlineMockTest.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR /'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'OnlineMockTest.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases




# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

