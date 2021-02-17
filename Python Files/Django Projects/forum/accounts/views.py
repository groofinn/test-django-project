from blogs.models import Blog
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import generic


# just renders index page
def index(request):
    return render(request, 'accounts/index.html')

# simple automated login view
class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

#simple automated logout view
class UserLogoutView(LogoutView):
    template_name = 'accounts/logout.html'

# takes args from UserCreationForm and creates user if everything is valid
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
    # else rerenders form
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

# gets all existing users and returns them in table
class UsersView(generic.ListView):
    template_name = 'accounts/users.html'
    context_object_name = 'users_list'
    paginate_by = 10
    def get_queryset(self):
        return User.objects.all().order_by('date_joined')

# renders detail page for every user by getting user's blog info
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

# you have to be logged in to access this page
@login_required
# here you can manage your account
def settings(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        user.delete()
        return redirect('accounts:index')
    return render(request, 'accounts/settings.html')