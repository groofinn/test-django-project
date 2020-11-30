from django.urls import path

from . import views

app_name = 'blogs'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    #path('auth/', views.auth, name='auth'),
    path('reg/', views.reg, name='reg'),
    #path('author/', views.AuthorView.as_view(), name='author'),
]
