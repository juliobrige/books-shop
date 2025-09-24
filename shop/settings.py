
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-b16%oq(s39*-q8_adid#t@@(etmr*a4mmj@&1=4mm#*6be3zhr'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
CORS_ALLOW_ALL_ORIGINS = True



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "django_filters",

    'phonenumber_field',
    'django_countries',
    # Documentação
    "drf_spectacular",
    "drf_spectacular_sidecar",

    # Nossos apps
    "api",
    "courses",
    "users",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # <-- ADICIONE ESTA LINHA
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'shop.wsgi.application'

DB_ENGINE = os.getenv("DB_ENGINE", "sqlite") # "sqlite" é o padrão

if DB_ENGINE == "sqlite":
    # Configuração para SQLite3 ✅
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    # A sua configuração original para PostgreSQL
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB"),
            "USER": os.getenv("POSTGRES_USER"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
            "HOST": os.getenv("POSTGRES_HOST"),
            "PORT": int(os.getenv("POSTGRES_PORT")),
            "OPTIONS": {"options": "-c client_encoding=UTF8"},
        }
    }
# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend"
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

SPECTACULAR_SETTINGS = {
        'TITLE': 'Books-Shop & LMS API',
    'DESCRIPTION': """
Documentação detalhada para a API da plataforma Books-Shop.

Funcionalidades principais:
- 📖 **Loja:** Catálogo de livros, carrinho de compras e sistema de pedidos.
- 🎓 **Cursos:** Catálogo de cursos, matrículas e acompanhamento de progresso.
- 👤 **Utilizadores:** Autenticação, registo e gestão de perfis.
    """,
    'VERSION': '0.2.0', # Use a versão atual do seu projeto
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_DIST': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
    "CONTACT": {
        "name": "Equipe Books Shop",
        "email": "suporte@booksshop.dev",
        "url": "https://booksshop.dev",
    },
    "LICENSE": {"name": "MIT"},
    "SERVE_INCLUDE_SCHEMA": False,  # manter schema separado de /api/schema/
    "SCHEMA_PATH_PREFIX": r"/(store|courses|users|api)",  # opcional: filtra o que entra no schema

    # UX do Swagger
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "displayRequestDuration": True,
        "filter": True,                 # caixa de filtro na barra superior
        "persistAuthorization": True,   # mantém o Bearer token entre reloads
        "tryItOutEnabled": True,        # botão "Try it out" por padrão
        "syntaxHighlight": {"activated": True},
    },

    # Usa assets locais (sem depender de CDN) via sidecar
    "SWAGGER_UI_DIST": "SIDECAR",  # requer drf_spectacular_sidecar
    "REDOC_DIST": "SIDECAR",
}
# --- CORS Headers ---
# Define quais origens (sites) podem aceder à nossa API
# Por agora, vamos permitir o endereço padrão de um projeto React/Vue/Angular
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173", # <-- GARANTA QUE ESTA LINHA EXISTE
    "http://127.0.0.1:5173", # <-- Adicione esta também por segurança
]
# Para um ambiente de desenvolvimento muito inicial, pode usar:
#CORS_ALLOW_ALL_ORIGINS = True


# --- Simple JWT ---
# Configurações para a duração e comportamento dos tokens
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60), # Duração do token de acesso
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),    # Duração do token de atualização
}

# --- Static & Media Files ---
# Configurações para ficheiros estáticos (CSS, JS) e de media (uploads de utilizadores)
STATIC_URL = 'static/'
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
