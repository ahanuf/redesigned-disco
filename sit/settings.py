import os
from pathlib import Path
from dotenv import load_dotenv
# from channels.auth import AuthMiddlewareStack
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable is not set")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "ALLOWED_HOSTS",
        "127.0.0.1,localhost"
    ).split(",")
    if host.strip()
]

# CSRF_COOKIE_SECURE = True  # CSRF cookies are only sent over HTTPS
# SESSION_COOKIE_SECURE = True  # Session cookies are only sent over HTTPS
# SECURE_SSL_REDIRECT = True  # Redirect HTTP to HTTPS
# SECURE_HSTS_SECONDS = 31536000  # Enable HTTP Strict Transport Security (HSTS)
# SECURE_HSTS_PRELOAD = True  # Preload HSTS
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Apply HSTS to subdomains as well
# SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevent browsers from interpreting files as something else
# X_FRAME_OPTIONS = 'DENY'  # Protect against clickjacking
# SECURE_BROWSER_XSS_FILTER = True  # Enable browser's XSS filtering
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition

INSTALLED_APPS = [
    # "daphne",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    
    'corsheaders',
    # "channels",
    'rest_framework',
    'rest_framework_simplejwt',
    "rest_framework_simplejwt.token_blacklist",
    'modelcluster',
    'taggit',
    "django_ckeditor_5",
    
    "app",
    'tasks.apps.TasksConfig',
    # 'chat', 
    "widget_tweaks",
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',          
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    "http://localhost:5173",
]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CSRF_TRUSTED_ORIGINS",
        "http://localhost:8000,https://localhost:8000"
    ).split(",")
    if origin.strip()
]

CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"

ROOT_URLCONF = 'sit.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                "app.views.categories",
            ],
        },
    },
]

WSGI_APPLICATION = 'sit.wsgi.application'
# ASGI_APPLICATION = "sit.asgi.application"

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'postdatabase'),
        'USER': os.getenv('POSTGRES_USER', 'ubun'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),
        'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
        'PORT': os.getenv('POSTGRES_PORT', '5432'),
    }
}

# Channel layer backed by Redis

# REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
# REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))

# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels_redis.core.RedisChannelLayer',
#         'CONFIG': {
#             'hosts': [(REDIS_HOST, REDIS_PORT)],
#         },
#     },
# }

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTHENTICATION_BACKEND = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

SITE_ID = 1
AUTH_USER_MODEL = 'auth.User'
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_LOGIN_METHODS = {"username", "email"} 
ACCOUNT_SIGNUP_FIELDS = ['email', 'username*', 'password1*', 'password2*']

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/accounts/login-redirect/"
LOGOUT_REDIRECT_URL = "/"
ACCOUNT_LOGIN_REDIRECT_URL = "/accounts/login-redirect/"
ACCOUNT_SIGNUP_REDIRECT_URL = "/accounts/login-redirect/"


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',),
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
}




SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    # "BLACKLIST_AFTER_ROTATION": True,
}


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "statics/"
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
STATICFILES_DIRS = [BASE_DIR / "static" ]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media/"



# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ✅ CACHING (REDIS)
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': f'redis://{REDIS_HOST}:{REDIS_PORT}/1',
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#         }
#     }
# }

# CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
# CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"



EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "127.0.0.1"
EMAIL_PORT = 1025

EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""

EMAIL_USE_TLS = False
EMAIL_USE_SSL = False



customColorPalette = [
    {"color": "hsl(4, 90%, 58%)", "label": "Red"},
    {"color": "hsl(340, 82%, 52%)", "label": "Pink"},
    {"color": "hsl(291, 64%, 42%)", "label": "Purple"},
    {"color": "hsl(262, 52%, 47%)", "label": "Deep Purple"},
    {"color": "hsl(231, 48%, 48%)", "label": "Indigo"},
    {"color": "hsl(207, 90%, 54%)", "label": "Blue"},
]
CKEDITOR_5_CONFIGS = {
    "default": {
        "language": {"ui": "en", "content": "en"},
        "toolbar": {
            "items": [
                "undo", "redo", "|",
                "heading", "|",
                "bold", "italic", "underline", "strikethrough", "highlight", "|",
                "subscript", "superscript", "removeFormat", "|",
                "fontSize", "fontFamily", "fontColor", "fontBackgroundColor", "|",
                "alignment", "|",
                "bulletedList", "numberedList", "todoList", "|",
                "outdent", "indent", "blockQuote", "horizontalLine", "|",
                "code", "codeBlock", "htmlEmbed", "sourceEditing", "|",
                "link", "insertImage", "mediaEmbed", "fileUpload", "|",
                "insertTable", "findAndReplace", "specialCharacters", "selectAll", "|",
                "showBlocks", "style", "pageBreak",
            ],
            "shouldNotGroupWhenFull": True,
        },
        "image": {
            "toolbar": [
                "imageTextAlternative", "|",
                "imageStyle:block", "imageStyle:side",
                "imageStyle:alignLeft", "imageStyle:alignCenter", "imageStyle:alignRight", "|",
                "resizeImage:50", "resizeImage:75", "resizeImage:100",
            ],
            "resizeUnit": "px",
            "styles": ["full", "side", "alignLeft", "alignCenter", "alignRight"],
        },
        "table": {
            "contentToolbar": [
                "tableColumn", "tableRow", "mergeTableCells",
                "tableProperties", "tableCellProperties", "toggleTableCaption",
            ],
            "tableProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
            "tableCellProperties": {
                "borderColors": customColorPalette,
                "backgroundColors": customColorPalette,
            },
        },
        "heading": {
            "options": [
                {"model": "paragraph", "title": "Paragraph", "class": "ck-heading_paragraph"},
                {"model": "heading1", "view": "h1", "title": "Heading 1", "class": "ck-heading_heading1"},
                {"model": "heading2", "view": "h2", "title": "Heading 2", "class": "ck-heading_heading2"},
                {"model": "heading3", "view": "h3", "title": "Heading 3", "class": "ck-heading_heading3"},
                {"model": "heading4", "view": "h4", "title": "Heading 4", "class": "ck-heading_heading4"},
                {"model": "heading5", "view": "h5", "title": "Heading 5", "class": "ck-heading_heading5"},
                {"model": "heading6", "view": "h6", "title": "Heading 6", "class": "ck-heading_heading6"},
            ],
        },
        "list": {
            "properties": {
                "styles": True,
                "startIndex": True,
                "reversed": True,
            },
        },
        "link": {
            "defaultProtocol": "https://",
        },
        "style": {
            "definitions": [
                {"name": "Article Category", "element": "h3", "classes": ["category"]},
                {"name": "Info Box", "element": "p", "classes": ["info-box"]},
                {"name": "Important Text", "element": "p", "classes": ["important-text"]},
                {"name": "Note", "element": "div", "classes": ["note"]},
            ],
        },
    }
}


