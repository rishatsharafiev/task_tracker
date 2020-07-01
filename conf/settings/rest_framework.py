from datetime import timedelta

from decouple import config


# # REST
# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticated',
#     ),
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'knox.auth.TokenAuthentication',
#         'rest_framework.authentication.SessionAuthentication',
#         'rest_framework.authentication.BasicAuthentication',
#     ),
#     'DEFAULT_THROTTLE_CLASSES': [
#         'rest_framework.throttling.AnonRateThrottle',
#         'rest_framework.throttling.UserRateThrottle'
#     ],
#     'DEFAULT_THROTTLE_RATES': {
#         'anon': '200/minute',
#         'user': '2000/minute'
#     }
# }

# # CORS
# CORS_ALLOW_CREDENTIALS = config('CORS_ALLOW_CREDENTIALS', cast=bool, default=True)
# CORS_ORIGIN_ALLOW_ALL = config('CORS_ORIGIN_ALLOW_ALL', cast=bool, default=True)

# REST_KNOX = {
#     'TOKEN_TTL': timedelta(days=28),
#     'USER_SERIALIZER': 'users.serializers.MiddleUserSerializer',
#     'AUTO_REFRESH': True,
#     'TOKEN_LIMIT_PER_USER': float('inf'),
#     'MIN_REFRESH_INTERVAL': 3600
# }

# SWAGGER_SETTINGS = {
#     'SECURITY_DEFINITIONS': {
#         "Token": {
#             "type": "apiKey",
#             "name": "Authorization",
#             "in": "header"
#         }
#     },
#     'LOGIN_URL': 'admin:login',
#     'LOGOUT_URL': 'admin:logout'
# }

# REDOC_SETTINGS = {
#     'LAZY_RENDERING': True,
#     'NATIVE_SCROLLBARS': True
# }
