from decouple import config


ENVIRONMENT = config('ENVIRONMENT')

if ENVIRONMENT in ['prod', 'stage']:
    EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# EMAIL
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool, default=True)
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', cast=str)
SERVER_EMAIL = config('SERVER_EMAIL', cast=str)
EMAIL_HOST = config('EMAIL_HOST', cast=str)
EMAIL_PORT = config('EMAIL_PORT', cast=int, default=587)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', cast=str)
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', cast=str)
