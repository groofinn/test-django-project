from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('settings/', views.settings, name='settings'),
    path('users/', views.UsersView.as_view(), name='users'),
    path('users/<str:username>/', views.detail, name='detail'),
]