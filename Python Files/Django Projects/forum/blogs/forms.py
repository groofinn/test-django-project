from django.forms import ModelForm

from .models import Blog
from django.contrib.auth.models import User

class BlogForm(ModelForm):
    class Meta:
        model = Blog
        exclude = ('user',)