from django.db import models
from django.conf import settings
import random

class Token(models.Model):
    token = models.CharField(max_length=32)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        str1 = '123456789'
        str2 = 'qwertyuiopasdfghjklzxcvbnm/*:#@!?&$'
        str3 = str2.upper()
        str4 = str1 + str2 + str3
        ls = list(str4)
        random.shuffle(ls)
        token = ''.join([random.choice(ls) for x in range(32)])
        self.token = token
        super().save(*args, **kwargs) 