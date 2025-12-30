from pathlib import Path
import os
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path( __file__ ).resolve( ).parent.parent

# Load environment variables from a local .env file if present (useful on PythonAnywhere)
load_dotenv(BASE_DIR / '.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Read SECRET_KEY from environment in production; fallback to the development key for local use
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-^yhjhum@rt2o(@hzfm@m34oym5g9!$00j8*wd01a&ge^x_sy5e')

# SECURITY WARNING: don't run with debug turned on in production!
# Use the DJANGO_DEBUG env var (set to 'True' for development)
def _bool_env(var, default=False):
    val = os.environ.get(var)
    if val is None:
        return default
    # Strip whitespace before interpreting truthy strings like 'True', ' true', or ' 1'
    return str(val).strip().lower() in ('1', 'true', 'yes', 'on')

DEBUG = _bool_env('DJANGO_DEBUG', True)

# Allow hosts via ALLOWED_HOSTS env var (comma-separated). Defaults to localhost and 127.0.0.1.
# Normalize by stripping whitespace and ignoring empty entries
ALLOWED_HOSTS = [h.strip() for h in os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',') if h.strip()]

# Safety check: require a strong SECRET_KEY when running in production
from django.core.exceptions import ImproperlyConfigured
if not DEBUG:
    if SECRET_KEY.startswith('django-insecure-') or len(SECRET_KEY) < 50:
        raise ImproperlyConfigured(
            "When DJANGO_DEBUG is False you must set a secure SECRET_KEY in the environment. \n"
            "Generate one locally with: python -c \"import secrets; print(secrets.token_urlsafe(50))\"\n"
            "Then set it in your hosting environment (do not commit it to the repository)."
        )

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join( BASE_DIR, 'staticfiles' )

# Use WhiteNoise for static files in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_DIRS = [
os.path.join( BASE_DIR, 'static' ),
# ... other directories if needed
]

MEDIA_ROOT = os.path.join( BASE_DIR, 'media' )
MEDIA_URL = '/media/'

INSTALLED_APPS = [
'django.contrib.admin',
'django.contrib.auth',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.messages',
'django.contrib.staticfiles',
'django_ckeditor_5',
'mtb_v5_app',
]

CKEDITOR_5_CONFIGS = {
'default': {
'toolbar'   : [
'heading', '|',
'bold', 'italic', 'underline', 'strikethrough', '|',
'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', '|',
'alignment', '|',
'bulletedList', 'numberedList', '|',
'outdent', 'indent', '|',
'link', 'blockQuote', '|',
'undo', 'redo'
],
'fontSize'  : {
'options': [ 9, 10, 11, 12, 13, 14, 15, 16, 18, 20, 22 ]
},
'fontFamily': {
'options': [
'default',
'Arial, Helvetica, sans-serif',
'Courier New, Courier, monospace',
'Georgia, serif',
'Times New Roman, Times, serif',
]
},
'contentsCss': ['/static/css/ckeditor-custom.css', '/static/css/admin-ckeditor.css'],

},
}

# Add media path for uploads if needed
CKEDITOR_5_UPLOAD_PATH = "uploads/"
CKEDITOR_5_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

MIDDLEWARE = [
'django.middleware.security.SecurityMiddleware',
'whitenoise.middleware.WhiteNoiseMiddleware',
'django.contrib.sessions.middleware.SessionMiddleware',
'django.middleware.common.CommonMiddleware',
'django.middleware.csrf.CsrfViewMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',
'django.contrib.messages.middleware.MessageMiddleware',
'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mtb_v5_settings.urls'

TEMPLATES = [
{
'BACKEND' : 'django.template.backends.django.DjangoTemplates',
'DIRS'    : [ BASE_DIR / 'templates' ],
'APP_DIRS': True,
'OPTIONS' : {
'context_processors': [
'django.template.context_processors.debug',
'django.template.context_processors.request',
'django.contrib.auth.context_processors.auth',
'django.contrib.messages.context_processors.messages',
],
},
},
]

WSGI_APPLICATION = 'mtb_v5_settings.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
#
DATABASES = {
'default': {
'ENGINE': 'django.db.backends.sqlite3',
'NAME'  : BASE_DIR / 'db.sqlite3',
}
}

# Optionally configure the database from DATABASE_URL env var (e.g., for production)
if os.environ.get('DATABASE_URL'):
    try:
        import dj_database_url
        DATABASES['default'] = dj_database_url.parse(os.environ['DATABASE_URL'], conn_max_age=600)
    except ImportError:
        # dj-database-url not installed; keep default sqlite DB
        pass

# DATABASES = {
#   'default': {
#     'ENGINE'  : 'django.db.backends.postgresql',  # Or 'django.db.backends.postgresql_psycopg2'
#     'NAME'    : 'mtb_v4_pgdb',
#     'USER'    : 'postgres',
#     'PASSWORD': 'postgres',
#     'HOST'    : 'localhost',  # Or the IP address of your PostgreSQL server
#     'PORT'    : '5432',
#   }
# }

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# CRISPY_TEMPLATE_PACK = 'uni_form'
# CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap3"
# CRISPY_TEMPLATE_PACK = "bootstrap3"

# email configuration settings
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'dtebar@gmail.com'
# EMAIL_HOST_PASSWORD = 'gaml xvnn vaar nyvy'
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = 'dtebar@top-quarks.com'

# email configuration settings
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# # EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'dtebar@gmail.com'
# EMAIL_HOST_PASSWORD = 'qjjw mcay bqgi vvbt'
# EMAIL_USE_TLS = True
# DEFAULT_FROM_EMAIL = 'dtebar@top-quarks.com'

# Logging configuration to suppress broken pipe errors
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'suppress_broken_pipe': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': lambda record: 'Broken pipe' not in record.getMessage()
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'filters': ['suppress_broken_pipe'],
        },
    },
    'loggers': {
        'django.server': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Production security settings (configure these via environment variables on PythonAnywhere):
# - Set DJANGO_DEBUG='False' in production
# - Set SECRET_KEY in env (must be long and random)
# - Set SESSION_COOKIE_SECURE='True' and CSRF_COOKIE_SECURE='True' when serving over HTTPS
# - Set SECURE_SSL_REDIRECT='True' and SECURE_HSTS_SECONDS to a reasonable value (e.g. 3600 or more) when behind HTTPS
SESSION_COOKIE_SECURE = _bool_env('SESSION_COOKIE_SECURE', False)
CSRF_COOKIE_SECURE = _bool_env('CSRF_COOKIE_SECURE', False)
SECURE_SSL_REDIRECT = _bool_env('SECURE_SSL_REDIRECT', False)
try:
    SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', '0'))
except ValueError:
    SECURE_HSTS_SECONDS = 0

# Additional HSTS settings configurable via environment variables
SECURE_HSTS_INCLUDE_SUBDOMAINS = _bool_env('SECURE_HSTS_INCLUDE_SUBDOMAINS', False)
SECURE_HSTS_PRELOAD = _bool_env('SECURE_HSTS_PRELOAD', False)
