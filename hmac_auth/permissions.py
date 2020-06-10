from rest_framework.permissions import BasePermission
from .models import Token
from .HMACToken import HmacToken, TokenPeriod
from django.contrib.auth import get_user_model

User = get_user_model()

class TokenPermission(BasePermission):
    message = 'Wrong or expired temporary token'

    def has_permission(self, request, view):
        if 'HMAC-Login' not in request.headers or 'HMAC-Times' not in request.headers or 'HMAC-Token' not in request.headers:
            return False
        token = request.headers['HMAC-Token']
        login = request.headers['HMAC-Login']
        times = request.headers['HMAC-Times']
        users = User.objects.filter(username=login).all()
        if len(users) == 0:
            return False
        tokens = Token.objects.filter(user=users[0]).all() 
        if len(tokens) == 0:
            return False
        crypt = HmacToken(tokens[0].token, TokenPeriod.day)
        return crypt.checkToken(login, times, token)

    def has_object_permission(self, request, view, user):
        if 'HMAC-Login' not in request.headers or 'HMAC-Times' not in request.headers or 'HMAC-Token' not in request.headers:
            return False
        token = request.headers['HMAC-Token']
        login = request.headers['HMAC-Login']
        times = request.headers['HMAC-Times']
        tokens = Token.objects.filter(user=user).all() 
        if len(tokens) == 0:
            return False
        crypt = HmacToken(tokens[0].token, TokenPeriod.day)
        return crypt.checkToken(login, times, token)
        
        

