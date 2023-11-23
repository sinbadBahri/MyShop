from .base import *

# Databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Cores Headers

CORS_ALLOW_ALL_ORIGINS = True
