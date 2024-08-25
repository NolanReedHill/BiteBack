"""
Django settings for biteback project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
import secrets
from pathlib import Path
from dotenv import load_dotenv
import django_heroku
import dj_database_url

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    default=secrets.token_urlsafe(nbytes=64),
)


# SECURITY WARNING: don't run with debug turned on in production!
IS_HEROKU_APP = "DYNO" in os.environ and not "CI" in os.environ

if not IS_HEROKU_APP:
    DEBUG = True
    ALLOWED_HOSTS = ["127.0.0.1"]
    ALLOWED_HOSTS = ["127.0.0.1"]

if IS_HEROKU_APP:
    ALLOWED_HOSTS = ['localhost', 'biteback-8ae7ecd5218d.herokuapp.com', 'biteback2-145244a0becf.herokuapp.com']
else:
    ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "django.contrib.messages",
    "django.contrib.sites",
    "mainApp",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "django_bootstrap5",
    "storages",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "biteback.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "biteback.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
if IS_HEROKU_APP:
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=True,
        )
    }

    LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "DEBUG"),
            },
        },
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": os.environ["db_name"],
            "USER": os.environ["db_username"],
            "PASSWORD": os.environ["db_password"],
            "HOST": "127.0.0.1",
            "PORT": "5432",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# STATIC_URL = "static/"
# STATIC_ROOT = BASE_DIR / 'staticfiles'
"""
STORAGES = {
    #Enable WhiteNoise's GZip and Brotli compression of static assets:
    #https://whitenoise.readthedocs.io/en/latest/django.html#add-compression-and-caching-support
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage", 
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
"""

# S3 Settings
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_STORAGE_BUCKET_NAME = "cs3240-biteback"
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")
# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None

GOOGLE_PLACES_API_KEY = os.environ["GOOGLE_PLACES_API_KEY"]


STATIC_URL = "static/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "mainApp", "static"),
]


DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

WHITENOISE_KEEP_ONLY_HASHED_FILES = False


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "APP": {
            "client_id": os.environ["CLIENT_ID"],
            "secret": os.environ["CLIENT_SECRET"],
        },
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    }
}

SITE_ID = 2

LOGIN_REDIRECT_URL = "/index"
# LOGOUT_REDIRECT_URL = "login"

AUTH_USER_MODEL = "mainApp.User"

SESSION_COOKIE_HTTPONLY = False
SESSION_COOKIE_SECURE = False
