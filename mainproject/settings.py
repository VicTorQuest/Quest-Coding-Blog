"""
Django settings for mainproject project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
from django.contrib.messages import constants as messages
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG =  True#str(os.environ.get('DEBUG')) == '1'

ALLOWED_HOSTS = []

if not DEBUG:
    ALLOWED_HOSTS += [os.environ.get('ALLOWED_HOSTS')]

AUTH_USER_MODEL = 'mainapp.User'
# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    
    #all auth app config
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.github',

    #my apps
    'mainapp.apps.MainappConfig',
    'blog.apps.BlogConfig',
    'newsletter.apps.NewsletterConfig',
    'store.apps.StoreConfig',

    #installed packages
    'rest_framework',
    'crispy_forms',
    'django_social_share',
    'ckeditor',
    'ckeditor_uploader',
    'hitcount',
    'django_countries',
    'captcha',
    'maintenance_mode',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'maintenance_mode.middleware.MaintenanceModeMiddleware',
]


ROOT_URLCONF = 'mainproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "maintenance_mode.context_processors.maintenance_mode",
            ],
        },
    },
]


AUTHENTICATION_BACKENDS = [
    
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'mainproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: 'alert-danger'
}

CKEDITOR_BASEPATH = '/static/ckeditor/ckeditor/'
CKEDITOR_UPLOAD_PATH = "post_images/"
CKEDITOR_IMAGE_BACKEND = 'pillow'

CKEDITOR_CONFIGS = {
    'awesome_ckeditor': {
        'toolbar': 'full',
    },

    'default': {
        'toolbar': 'full',
    },
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "dark_mode_theme": "darkly",
}

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static/')]

if DEBUG:
    MEDIA_URL = 'media/'
    MEDIA_ROOT = BASE_DIR / 'media/'

# MY EMAIL SETTING

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
APPLICATION_EMAIL = os.environ.get('APPLICATION_EMAIL')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')


DEFAULT_FILE_STORAGE = 'mainproject.storages.MediaStore'

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_QUERYSTRING_AUTH = False 
AWS_DEFAULT_ACL = 'public-read'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_ID = 2
LOGIN_REDIRECT_URL = '/my-account/'
LOGIN_URL = '/my-account'
# Provider specific settings
ACCOUNT_LOGOUT_REDIRECT_URL = 'my_account'
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_STORE_TOKENS = True

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': os.environ.get('GOOGLE_CLIENT_ID'),
            'secret': os.environ.get('GOOGLE_SECRET_KEY'),
            'key': ''
        },

        'SCOPE': [
            'profile',
            'email',
        ],

        'AUTH_PARAMS': {
            'access_type': 'online',
        }

    },
    'github': {
        'SCOPE': [
            'user',
            'repo',
            'read:org',
        ],
    }
}



JAZZMIN_SETTINGS = {
     "site_title": "Quest Coding Blog",
     "site_header": "Quest Coding Admin",
     "site_brand": "Quest Coding Blog",
     "site_logo": "favicon.ico",
    #  "login_logo": None,
    "site_logo_classes": "img-circle",
    "site_icon": 'favicon.ico',
    "welcome_sign": "Welcome to the admin",
    "copyright": "Quest Coding",
    "search_model": "mainapp.User",
    "user_avatar": 'avatar',

    "topmenu_links": [

        {"model": "mainapp.User"},
        {"model": "blog.Post"},

        {"app": "newsletter"},
        {"model": "store.Order"},
        
    ],


    "navigation_expanded": False,
    "hide_apps": ["auth"],


    "icons": {
        "mainapp.user": "fas fa-user",
        "account.emailaddress": "fas fa-envelope",
        "blog.category": "fas fa-object-ungroup",
        "blog.comment": "fas fa-comments",
        "blog.author": "fas fa-user-edit",
        "blog.post": "fas fa-pen-square",
        "blog.featuredpost": "fas fa-pen-square",
        "blog.subcategory": "fas fa-object-group",
        "hitcount.blacklistip": "fas fa-times-circle",
        "hitcount.blacklistuseragent": "fas fa-times-circle",
        "hitcount.hitcount": "fas fa-sort-numeric-up",
        "hitcount.hit": "fas fa-mouse",
        "newsletter.mailmessage": "fas fa-mail-bulk",
        "newsletter.subscriber": "fas fa-paper-plane",
        "newsletter.unsubscribedemail": "fas fa-minus-circle",
        "sites.site": "fas fa-globe",
        "socialaccount.socialaccount": "fas fa-user",
        "socialaccount.socialtoken": "fas fa-check",
        "socialaccount.socialapp": "fas fa-globe",
        "store.customer": "fas fa-user",
        "store.orderitem": "fas fa-shopping-basket",
        "store.order": "fas fa-shopping-cart",
        "store.product": "fas fa-gift",
        "store.review": "fas fa-comments",
        "store.billingaddress": "fas fa-shipping-fast",
        "store.refund": "fas fa-undo-alt"
    },


}

# JAZZMIN_SETTINGS["show_ui_builder"] = True

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-info",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "darkly",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": True
}

RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')


RECAPTCHA_REQUIRED_SCORE = 0.85


MAINTENANCE_MODE_IGNORE_ADMIN_SITE = True
MAINTENANCE_MODE_IGNORE_URLS = ['/toggle-maintenance/', '/getting_cart_total/', '/maintenance-switch/']


if DEBUG:
    DOMAIN_NAME = 'http://' + '127.0.0.1:8000'
else:
    DOMAIN_NAME = "https://" + str(ALLOWED_HOSTS[0])