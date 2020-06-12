import hashlib
import enum
import calendar
from datetime import datetime
from django.conf import settings

today = datetime.now().date()

class TokenPeriod(enum.IntEnum):
    minute = 60
    hour = minute * 60
    day = hour * 24
    week = 7 * day
    month = calendar.monthrange(today.year, today.month)[1] * day
    year = 366 * day if calendar.isleap(today.year) else 365 * day

class HmacToken:
    def __init__(self, salt, period, hash_func):
        self.salt = salt
        self.period = period
        self.hash_func = hash_func

    def getToken(self, login):
        times = str(int(datetime.today().timestamp()))
        h = hashlib.new(self.hash_func)
        h.update((login + times + self.salt).encode())
        return (times, h.hexdigest())

    def checkToken(self, login, times, token):
        h = hashlib.new(self.hash_func)
        h.update((login + times + self.salt).encode())
        predict = h.hexdigest()
        return token == predict and datetime.today().timestamp() - int(times) <= self.period