import dj_database_url
import django

from .base_settings import *

ALLOWED_HOSTS = ['*']

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'wassignment', 'media')
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s: %(message)s'
        },
        'simple': {
            'format': '%(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO'
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'WARNING',
            'propagate': False
        },
        '': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False
        }
    }
}

DATABASES['default'] = dj_database_url.config() if os.environ.get('DATABASE_URL') else DATABASES['default']
