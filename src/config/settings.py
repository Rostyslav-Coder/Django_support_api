"""Django settings for config project."""

from datetime import timedelta
from distutils.util import strtobool
from os import getenv
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
SRC_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = SRC_DIR.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv("DJANGO_SECRET_KEY", default="invalid")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = strtobool(getenv("DJANGO_DEBUG", default="false"))
ALLOWED_HOSTS = ["*"]


# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_yasg",
]

LOCAL_APPS = [
    "authentication.apps.AuthenticationConfig",
    "tickets.apps.TicketsConfig",
    "users.apps.UsersConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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

WSGI_APPLICATION = "config.wsgi.application"


# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ROOT_DIR / "db.sqlite3",
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # noqa: E501
    },
]


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


POKEAPI_BASE_URL = getenv("POKEAPI_BASE_URL", default="invalid")


AUTH_USER_MODEL = "users.User"


REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

if DEBUG is True:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"].append(
        "rest_framework.renderers.BrowsableAPIRenderer",
    )

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(
        seconds=int(getenv("JWT_ACCESS_TOKEN_LIFETIME", default=260))
    ),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        seconds=int(getenv("JWT_REFRESH_TOKEN_LIFETIME", default=43200))
    ),
    "AUTH_HEADER_TYPES": (getenv("JWT_AUTH_HEADER_TYPES", default="Bearer "),),
}

CELERY_BROKER_URL = getenv(
    "CELERY_BROKER_URL", default="redis://broker:6379/0"
)
