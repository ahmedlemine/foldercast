from pathlib import Path
import environ

env = environ.Env(DEBUG=(bool, False))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Take environment variables from .env file
environ.Env.read_env(Path(BASE_DIR / ".env"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = ["localhost"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Thrid Party
    "crispy_forms",
    "crispy_bootstrap5",
    # Local
    "core.apps.CoreConfig",
    "accounts.apps.AccountsConfig",
    "feeds",
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

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = env("TIME_ZONE", default="UTC")

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_URL = "static/"
STATIC_ROOT = "static_cdn"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTH_USER_MODEL = "accounts.CustomUser"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"


###############################
# FolderCast specific settings:#
###############################

# FEEDS APP SETTINGS
# If you change this setting you must also chgnge the
# mount point in Docker container config to match this.
LIBRARY_ROOT = BASE_DIR / "library"
LIBRARY_URL = "library/"

SERVER_PORT = env("SERVER_PORT", default="8800")

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[])

ADMINS = [
    (env("ADMIN_NAME"), env("ADMIN_EMAIL")),
]


AUDIO_EXTENSIONS = [
    "3gp",
    "aa",
    "aac",
    "aax",
    "aiff",
    "alac",
    "amr",
    "ape",
    "au",
    "awb",
    "dss",
    "dvf",
    "flac",
    "gsm",
    "iklax",
    "ivs",
    "m4a",
    "m4b",
    "m4p",
    "mmf",
    "movpkg",
    "mp1",
    "mp2",
    "mp3",
    "mpc",
    "msv",
    "nmf",
    "ogg",
    "oga",
    "mogg",
    "opus",
    "rarm",
    "raw",
    "rf64",
    "sln",
    "tta",
    "voc",
    "vox",
    "wav",
    "wma",
    "wv",
    "webm",
    "8svx",
    "cda",
]

AUDIO_MIME_TYPES = {
    "3gp": "audio/3gpp",
    "aa": "audio/audible",
    "aac": "audio/aac",
    "aax": "audio/x-aax",
    "aiff": "audio/aiff",
    "alac": "audio/alac",
    "amr": "audio/amr",
    "ape": "audio/ape",
    "au": "audio/basic",
    "awb": "audio/amr-wb",
    "dss": "audio/x-dss",
    "dvf": "audio/x-dvf",
    "flac": "audio/flac",
    "gsm": "audio/x-gsm",
    "iklax": "audio/x-iklax",
    "ivs": "audio/x-ivs",
    "m4a": "audio/mp4",
    "m4b": "audio/mp4",
    "m4p": "audio/mp4",
    "mmf": "audio/x-mmf",
    "movpkg": "application/vnd.apple.mpegurl",
    "mp1": "audio/mpeg",
    "mp2": "audio/mpeg",
    "mp3": "audio/mpeg",
    "mpc": "audio/x-musepack",
    "msv": "audio/x-msv",
    "nmf": "audio/x-nmf",
    "ogg": "audio/ogg",
    "oga": "audio/ogg",
    "mogg": "audio/ogg",
    "opus": "audio/opus",
    "rarm": "audio/x-pn-realaudio",
    "raw": "audio/x-raw",
    "rf64": "audio/rf64",
    "sln": "audio/x-sln",
    "tta": "audio/x-tta",
    "voc": "audio/x-voc",
    "vox": "audio/x-voxware",
    "wav": "audio/wav",
    "wma": "audio/x-ms-wma",
    "wv": "audio/x-wavpack",
    "webm": "audio/webm",
    "8svx": "audio/8svx",
    "cda": "application/x-cdf",
}
