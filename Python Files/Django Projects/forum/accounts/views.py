from blogs.models import Blog
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import generic


def index(request):
    return render(request, 'accounts/index.html')

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    def get_success_url(self):
        return reverse('accounts:index')

class UserLogoutView(LogoutView):
    template_name = 'accounts/logout.html'

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('accounts:index')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def settings(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        user.delete()
        return redirect('accounts:index')
    return render(request, 'accounts/settings.html')

class UsersView(generic.ListView):
    template_name = 'accounts/users.html'
    context_object_name = 'users_list'
    paginate_by = 10
    def get_queryset(self):
        return User.objects.all().order_by('date_joined')

def detail(request, username):
    user_info = User.objects.get(username=username)
    user_id = user_info.id
    blog_list = Blog.objects.filter(user=user_id)
    paginator = Paginator(blog_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request, 'accounts/detail.html',
        {'user': user_info, 'page_obj': page_obj}
    )