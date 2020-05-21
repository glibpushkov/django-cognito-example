import os
import json
from urllib import request

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'w3f6qk5c8g747+r@%=-_wjw5)b5&8x7^n!a3=b_8)!8z-8h!7('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.RemoteUserBackend',
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'django_cognito_example.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_cognito_example.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

AUTH_USER_MODEL = 'account.User'



REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'core.api.permissions.DenyAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
}


COGNITO_AWS_REGION = 'eu-central-1'
COGNITO_USER_POOL = 'eu-central-1_bUFIXsrqe'
# Provide this value (id of Cognito App Client) if `id_token` is used for authentication (it contains 'aud' claim).
# `access_token` doesn't have it, in this case keep the COGNITO_AUDIENCE empty
COGNITO_AUDIENCE = '2bdgd681nmmnickj0coq0j1oq1'
COGNITO_POOL_URL = None  # will be set few lines of code later, if configuration provided

rsa_keys = {}
# To avoid circular imports in future, we keep this logic here.
# On django init we download jwks public keys which are used to validate jwt tokens.
# For now there is no rotation of keys (and Cognito haven't still implemented it...)
if COGNITO_AWS_REGION and COGNITO_USER_POOL:
    COGNITO_POOL_URL = 'https://cognito-idp.{}.amazonaws.com/{}'.format(COGNITO_AWS_REGION, COGNITO_USER_POOL)
    pool_jwks_url = COGNITO_POOL_URL + '/.well-known/jwks.json'
    jwks = json.loads(request.urlopen(pool_jwks_url).read())
    rsa_keys = {key['kid']: json.dumps(key) for key in jwks['keys']}


JWT_AUTH = {
    'JWT_PAYLOAD_GET_USERNAME_HANDLER': 'core.api.jwt.get_username_from_payload_handler',
    'JWT_DECODE_HANDLER': 'core.api.jwt.cognito_jwt_decode_handler',
    'JWT_PUBLIC_KEY': rsa_keys,
    'JWT_ALGORITHM': 'RS256',
    'JWT_AUDIENCE': COGNITO_AUDIENCE,
    'JWT_ISSUER': COGNITO_POOL_URL,
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}
