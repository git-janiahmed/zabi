from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "k**pryirge11f_13q=zty7yxstp5$zgo*=3k@u$l1xh6-pnvdf"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# ALLOWED_HOSTS = ["happytyms.in", "www.happytyms.in", "89.116.34.32"]

ALLOWED_HOSTS = [
    "89.116.34.32",
    "happytyms.in",
]

SECURE_SSL_REDIRECT = True
# SECURE_SSL_REDIRECT = True
# SECURE_SSL_CERTIFICATE = "/ssl/certificate.crt"
# SECURE_SSL_KEY = "/ssl/private.key"
# Application definition

INSTALLED_APPS = [
    "myapp.apps.MyappConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rangefilter",
    "django_extensions",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "myproject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "myapp.context_processors.card_data",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "myproject.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
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
SESSION_COOKIE_SECURE = True

# Optionally, set CSRF cookie secure flag to True if your site is served over HTTPS
CSRF_COOKIE_SECURE = True

RAZORPAY_API_KEY = "rzp_test_rjozYzFtHN9E9n"
RAZORPAY_API_SECRET = "8Arwk9pGfxy70LNS1SRhjbVr"
FACEBOOK_ACCESS_TOKEN = "EAAExpDusZCp4BOzBUL8y5OBzRsDHTZCBgzWRo8HQhDoCHXYpioHPZBRZAKZBj5VMhZC3aXEsXZCso05ZBJtC6SJsKlCU37dsdnH9NApT2W9qG3tfgPYoCZCvbcUsS6GNWoTTEZC66HdmemkaVd3F3d66vpjiZCZCwSMdleVxhHxKOfHWDU5vRUCoxDzZBSZBZBednIOv5grnQbMHISGvg0hiT67RTM3"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]


MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
