from django.urls import path

from . import views

# name for fast referring
app_name = 'blogs'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('creation/', views.creation, name='creation'),
]