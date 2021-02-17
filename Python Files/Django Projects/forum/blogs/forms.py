from django.forms import ModelForm

from .models import Blog
from django.contrib.auth.models import User

# creates blog by sending and accepting blog information
class BlogForm(ModelForm):
    class Meta:
        model = Blog
        exclude = ('user',)