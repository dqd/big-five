import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent


def env_flag(name: str) -> bool:
    return os.environ.get(name, "").lower() in {"1", "true", "yes", "on"}


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env_flag("DEBUG")

# SECURITY WARNING: set the SECRET_KEY environment variable in production!
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-mwui+-qa5x+3pdge@r60&@b%qfvqfx^(32u#@#o!+!7#_ntksl"
)

ALLOWED_HOSTS = [
    "localhost",
    "big-five.cz",
]
CSRF_TRUSTED_ORIGINS = [
    "https://big-five.cz",
]

# Application definition

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "bigfive.b5",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")
    # The toolbar is shown to everyone, as the development server runs in Docker
    # and the client address is therefore not predictable.
    DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG}

ROOT_URLCONF = "bigfive.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "bigfive.wsgi.application"

# Database
# https://docs.djangoproject.com/en/stable/ref/settings/#databases

# SQLite does not create missing directories, so make sure the data directory exists.
DATA_DIR = BASE_DIR.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": DATA_DIR / "db.sqlite3",
    }
}

# Internationalization
# https://docs.djangoproject.com/en/stable/topics/i18n/

LOCALE_PATHS = [
    BASE_DIR / "locale",
]
LANGUAGE_CODE = "cs"
LANGUAGES = [
    ("cs", "česky"),
    ("en", "English"),
]

TIME_ZONE = "Europe/Prague"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/stable/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/stable/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
