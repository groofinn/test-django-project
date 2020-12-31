import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    blog_name = models.CharField(max_length=200)
    blog_text = models.CharField(max_length=9999)
    pub_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    def __str__(self):
        return self.blog_name