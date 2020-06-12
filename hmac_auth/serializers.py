from rest_framework import serializers
from .HMACToken import HmacToken, TokenPeriod
from .models import Token
from django.conf import settings

class TokenSerializer(serializers.BaseSerializer):
    login = serializers.CharField(max_length=255)
    times = serializers.CharField(max_length=255)
    token = serializers.CharField(max_length=256)

    def __init__(self, *args, **kwargs):
        kwargs['data'] = {}
        if 'user' in kwargs:
           kwargs['data']['user'] = kwargs['user']
        kwargs.pop('user', None)
        super().__init__(**kwargs)

    def to_representation(self, data):
        output = {}
        output['login'] = self.login
        output['times'] = self.times
        output['token'] = self.token
        return output

    def to_internal_value(self, data):
        if 'user' not in data:
            raise serializers.ValidationError({"error" : "User is missing"})
        HMAC_PERIOD = getattr(settings, 'HMAC_PERIOD', TokenPeriod.day)
        HMAC_HASH_FUNC = getattr(settings, 'HMAC_HASH_FUNC', 'md5')
        output = {}
        user = data['user']
        tokens = Token.objects.filter(user=user).all()
        token = '' 
        if len(tokens) == 0:
            obj = Token.objects.create(user=user)
            obj.save()
            token = obj.token
        else:
            token = tokens[0].token
        login = user.username
        crypt = HmacToken(token, HMAC_PERIOD, HMAC_HASH_FUNC)
        times, temp_token = crypt.getToken(login)
        self.login = login
        self.times = times
        self.token = temp_token
        return self