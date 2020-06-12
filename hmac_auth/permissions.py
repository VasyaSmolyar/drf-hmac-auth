from rest_framework.permissions import BasePermission
from .models import Token
from .HMACToken import HmacToken, TokenPeriod
from django.contrib.auth import get_user_model
from django.conf import settings

HMAC_LOGIN_HEADER = getattr(settings, 'HMAC_LOGIN_HEADER', 'HMAC-Login')
HMAC_TOKEN_HEADER = getattr(settings, 'HMAC_TOKEN_HEADER', 'HMAC-Token')
HMAC_TIMES_HEADER = getattr(settings, 'HMAC_TOKEN_HEADER', 'HMAC-Times') 
HMAC_PERIOD = getattr(settings, 'HMAC_PERIOD', TokenPeriod.day)
HMAC_HASH_FUNC = getattr(settings, 'HMAC_HASH_FUNC', 'md5')

User = get_user_model()

class TokenPermission(BasePermission):
    message = 'Wrong or expired temporary token'

    def has_permission(self, request, view):
        if 'HMAC-Login' not in request.headers or 'HMAC-Times' not in request.headers or 'HMAC-Token' not in request.headers:
            return False
        token = request.headers[HMAC_TOKEN_HEADER]
        login = request.headers[HMAC_LOGIN_HEADER]
        times = request.headers[HMAC_TIMES_HEADER]
        users = User.objects.filter(username=login).all()
        if len(users) == 0:
            return False
        tokens = Token.objects.filter(user=users[0]).all() 
        if len(tokens) == 0:
            return False
        crypt = HmacToken(tokens[0].token, HMAC_PERIOD, HMAC_HASH_FUNC)
        return crypt.checkToken(login, times, token)

    def has_object_permission(self, request, view, user):
        if 'HMAC-Login' not in request.headers or 'HMAC-Times' not in request.headers or 'HMAC-Token' not in request.headers:
            return False
        token = request.headers[HMAC_TOKEN_HEADER]
        login = request.headers[HMAC_LOGIN_HEADER]
        times = request.headers[HMAC_TIMES_HEADER]
        tokens = Token.objects.filter(user=user).all() 
        if len(tokens) == 0:
            return False
        crypt = HmacToken(tokens[0].token, HMAC_PERIOD, HMAC_HASH_FUNC)
        return crypt.checkToken(login, times, token)
        
        

