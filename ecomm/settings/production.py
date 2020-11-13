"""
Django settings for ecomm project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8h0$q!s_7scv&d0sptxza-6t*=r_ktr8u$6hh662g=jmc4(h4h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',

    ## Session!
    'django.contrib.sessions',

    'django.contrib.messages',
    'django.contrib.staticfiles',

    # our apps!
    'addresses',
    'accounts',
    'analytics',
    'billing',
    'carts',
    'marketing',
    'orders',
    'products',
    'search',
    'tags',

]

AUTH_USER_MODEL = 'accounts.User'  # changes the built-in user model to ours

MAILCHIMP_API_KEY = "c3727fd5ee87761ea62e6e629bf63558-us2"
MAILCHIMP_DATA_CENTER = "us2"
MAILCHIMP_EMAIL_LIST_ID = "c35d4fd9fa"

FORCE_SESSION_TO_ONE = False
FORCE_INACTIVE_USER_ENDSESSION = False

STRIPE_SECRET_KEY = 'sk_test_51HmCc1Lp7u52kdKryw1nKeAjvR51vJww9gHTbNm6OZuk4pq26dKQT1Qv2tbdcaMaHF7oSf0kdb8ovkEjaK5ael4X00TiJhLpJW'
STRIPE_PUB_KEY = 'pk_test_51HmCc1Lp7u52kdKrJKoYnLkrB7Tb8oXLLs2mSRrOqqKN4o7ASWXWp54iDc4osi1Z1xDooarv1z6VlVz1ctSoEe9T00KAIxZLed'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

ROOT_URLCONF = 'ecomm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # 미디어 파일 불러올 수 있도록 해주는 context_processors 활성화 후 {{ MEDIA_URL }}로 불러오기 쌉가능
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecomm.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static_my_proj")
]
STATIC_ROOT = os.path.join(BASE_DIR, "static_root")

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, "media_root")

CORS_REPLACE_HTTPS_REFERER = True
HOST_SCHEME = "https://"
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 1000000
SECURE_FRAME_DENY = True
