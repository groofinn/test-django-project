import datetime

from django.db import models
from django.utils import timezone

class Author(models.Model):
    author_name = models.CharField(max_length=200)
    first_auth_date = models.DateTimeField(auto_now_add=True)
    author_pass = models.CharField(max_length=200)
    def __str__(self):
        return self.author_name

class Blog(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    blog_name = models.CharField(max_length=200)
    blog_text = models.CharField(max_length=9999)
    pub_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.blog_name