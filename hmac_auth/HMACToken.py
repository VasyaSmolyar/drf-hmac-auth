import hashlib
import enum
import calendar
from datetime import datetime

today = datetime.now().date()

class TokenPeriod(enum.IntEnum):
    minute = 60
    hour = minute * 60
    day = hour * 24
    week = 7 * day
    month = calendar.monthrange(today.year, today.month)[1] * day
    year = 366 * day if calendar.isleap(today.year) else 365 * day

class HmacToken:
    def __init__(self, salt, period):
        self.salt = salt
        self.period = period

    def getToken(self, login):
        times = str(int(datetime.today().timestamp()))
        return (times, hashlib.md5((login + times + self.salt).encode()).hexdigest()) 

    def checkToken(self, login, times, token):
        predict = hashlib.md5((login + times + self.salt).encode()).hexdigest()
        return token == predict and datetime.today().timestamp() - int(times) <= self.period