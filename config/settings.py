from pathlib import Path
import os
from dotenv import load_dotenv

# 1) Rutas base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# 2) Carga variables de .env (solo para desarrollo/compose)
load_dotenv(BASE_DIR / ".env")

# 3) Clave secreta y modo DEBUG
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-insecure")
DEBUG = os.getenv("DJANGO_DEBUG", "0") == "1"

# 4) Hosts permitidos (separados por comas en .env)
ALLOWED_HOSTS = os.getenv(
    "DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,0.0.0.0"
).split(",")

# 5) Aplicaciones instaladas (lo básico + admin)
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Tus apps
    "core",
]

# 6) Middleware (lo estándar de Django)
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# 7) URLs raíz
ROOT_URLCONF = "config.urls"

# 8) Templates (carga desde /templates y de las apps)
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # crea esta carpeta si la usas
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

# 9) ASGI/WSGI
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# 10) Base de datos: Postgres vía .env o fallback a SQLite
if os.getenv("DATABASE_ENGINE") == "django.db.backends.postgresql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DATABASE_NAME", "appdb"),
            "USER": os.getenv("DATABASE_USER", "appuser"),
            "PASSWORD": os.getenv("DATABASE_PASSWORD", "apppass"),
            "HOST": os.getenv("DATABASE_HOST", "db"),  # servicio del compose
            "PORT": os.getenv("DATABASE_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "data" / "db.sqlite3",  # BD en archivo
        }
    }

# 11) Validación de contraseñas (por defecto)
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# 12) Idioma y zona horaria
LANGUAGE_CODE = "es-es"
TIME_ZONE = "Europe/Madrid"
USE_I18N = True
USE_TZ = True

# 13) Archivos estáticos y media
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"       # donde se colectan para prod
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"              # subidas de usuarios

# 14) Cookies/seguridad básica (mejoras cuando DEBUG=0)
CSRF_TRUSTED_ORIGINS = os.getenv(
    "DJANGO_CSRF_TRUSTED",
    "http://localhost,http://127.0.0.1"
).split(",")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")  # útil tras Nginx/proxy

# 15) Logging mínimo (ver errores en consola del contenedor)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}

# 16) Clave primaria por defecto
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
