"""
Django settings for blog_avg project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path
from django.core.management.utils import get_random_secret_key
import sys
# import dj_database_url
from dotenv import load_dotenv, find_dotenv
import dj_database_url



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

print(load_dotenv(find_dotenv()))
print(os.getenv("DATABASE_URL", None))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# I changed this to use random key but i might need to change it later since it may have trouble with coookies
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
AWS_S3_SIGNATURE_VERSION = os.getenv('AWS_S3_SIGNATURE_VERSION')
AWS_S3_FILE_OVERWRITE = os.getenv('AWS_S3_FILE_OVERWRITE') == 'True'
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = os.getenv('AWS_S3_VERIFY') == 'True'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

print(ALLOWED_HOSTS)
    
if DEBUG: 
  EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'   #During development only


DEVELOPMENT_MODE = os.getenv("DEVELOPMENT_MODE", "False") == "True"

# Application definition

INSTALLED_APPS = [
    #my apps

    'personal',
    'account',
    'blog',

    #system apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',

    #additional apps 
    # Rich Text Editor
    'ckeditor',
    'ckeditor_uploader',


    #Social sharing
    'django_social_share',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

ROOT_URLCONF = 'blog_avg.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
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

AUTH_USER_MODEL='account.Account'

WSGI_APPLICATION = 'blog_avg.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

if DEVELOPMENT_MODE is True:
     DATABASES = {
         "default": {
             "ENGINE": "django.db.backends.sqlite3",
             "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
         }
     }
elif len(sys.argv) > 0 and sys.argv[1] != 'collectstatic':
     if os.getenv("DATABASE_URL", None) is None:
         raise Exception("DATABASE_URL environment variable not defined")
     DATABASES = {
         "default": dj_database_url.parse(os.environ.get("DATABASE_URL")),
     }

# DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.sqlite3",
#             "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
#         }
#     }
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

STATICFILES_DIRS=[
  os.path.join(BASE_DIR, 'static'),
  os.path.join(BASE_DIR, 'media')
]
STATIC_URL = '/static/'
STATIC_ROOT=os.path.join(BASE_DIR, 'static_cdn')

# Following settings only make sense on production and may break development environments.
if not DEBUG:    # Tell Django to copy statics to the `staticfiles` directory
    # in your application directory on Render.
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # Turn on WhiteNoise storage backend that takes care of compressing static files
    # and creating unique names for each version so they can safely be cached forever.
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field


# Add these settings for serving static and media files from S3
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_QUERYSTRING_AUTH = False
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',  # Cache files for one day
}

# Media files (user-uploaded content)
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/media/"
MEDIAFILES_LOCATION='media'
DEFAULT_FILE_STORAGE = 'blog_avg.storage_backends.MediaStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CSRF_COOKIE_SECURE = True  # For secure (HTTPS) connections
CSRF_COOKIE_SAMESITE = 'None'  # Adjust based on your requirements
CSRF_TRUSTED_ORIGINS = os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS").split(",")

CKEDITOR_UPLOAD_PATH = 'blog/'  # Placeholder, will be dynamically determined by the upload_location function
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
        'height': 300,
        'width': '100%',
        # Other configuration options...
    },
    'blog': {
        'toolbarGroups': [
            {'name': 'document', 'groups': ['mode', 'document', 'doctools']},
            {'name': 'clipboard', 'groups': ['clipboard', 'undo']},
            {'name': 'editing', 'groups': ['find', 'selection', 'spellchecker', 'editing']},
            {'name': 'forms', 'groups': ['forms']},
            '/',
            {'name': 'basicstyles', 'groups': ['basicstyles', 'cleanup']},
            {'name': 'paragraph', 'groups': ['list', 'bidi', 'blocks', 'align', 'indent', 'paragraph']},
            {'name': 'links', 'groups': ['links']},
            {'name': 'insert', 'groups': ['insert']},
            '/',
            {'name': 'styles', 'groups': ['styles']},
            {'name': 'colors', 'groups': ['colors']},
            {'name': 'tools', 'groups': ['tools']},
            {'name': 'others', 'groups': ['others']},
            {'name': 'about', 'groups': ['about']}
        ],
        'removeButtons': 'ExportPdf,NewPage,Save,Print,Templates,Form,Radio,Checkbox,TextField,Textarea,HiddenField,Language,BidiRtl,BidiLtr,About',
        'toolbar': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms', 'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton', 'HiddenField']},
            '/',
            {'name': 'basicstyles', 'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph', 'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert', 'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'others', 'items': ['-']},
            {'name': 'about', 'items': ['About']},
        ],
        'height': 400,
        'width': '100%',
        'filebrowserUploadUrl': '/ckeditor/upload/',
        'filebrowserImageUploadUrl': '/ckeditor/upload/',
        'filebrowserUploadMethod': 'xhr',
        'uploadFields': {
            'image': {
                'path': CKEDITOR_UPLOAD_PATH,
            },
        },
        'extraPlugins': 'justify,liststyle,indent',
        # ... other CKEditor configuration options ...
    },
}

CKEDITOR_FILENAME_GENERATOR = 'blog_avg.utils.get_filename'
CKEDITOR_RESTRICT_BY_DATE = False
