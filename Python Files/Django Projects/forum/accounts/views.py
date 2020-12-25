from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse
from .models import User


def index(request):
    return render(request, 'accounts/index.html')

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    def get_success_url(self):
        return reverse('accounts:index')

class UserLogoutView(LogoutView):
    template_name = 'accounts/logout.html'