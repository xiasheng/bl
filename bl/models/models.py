
from django.db import models
import time

class User(models.Model):
    account_id = models.CharField(max_length=10)
    password = models.CharField(max_length=128)
    email = models.EmailField(null=True)
    nickname = models.CharField(max_length=64)
    gender = models.CharField(max_length=10)
    birthday = models.DateField(null=True)
    address = models.CharField(max_length=64)
    avatar = models.URLField(null=True)
    time_created = models.CharField(max_length=64, default=str(int(time.time())))

