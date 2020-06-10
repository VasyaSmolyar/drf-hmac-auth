from rest_framework import serializers
from .HMACToken import HmacToken, TokenPeriod
from .models import Token

class TokenSerializer(serializers.BaseSerializer):
    login = serializers.CharField(max_length=255)
    times = serializers.CharField(max_length=255)
    token = serializers.CharField(max_length=256)

    def to_representation(self, data):
        output = {}
        output['login'] = self.login
        output['times'] = self.times
        output['token'] = self.token
        return output

    def to_internal_value(self, data):
        if 'user' not in data:
            raise serializers.ValidationError({"error" : "User is missing"})
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
        crypt = HmacToken(token, TokenPeriod.day)
        times, temp_token = crypt.getToken(login)
        self.login = login
        self.times = times
        self.token = temp_token
        return self