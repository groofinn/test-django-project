import datetime

from django.db import models
from django.utils import timezone


class User(models.Model):
    user_name = models.CharField(max_length=200)
    user_password = models.CharField(max_length=200)
    first_auth_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    def __str__(self):
        return self.user_name