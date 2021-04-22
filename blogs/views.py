from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import generic

from .forms import BlogForm
from .models import Blog


# shows list of latest blogs
class IndexView(generic.ListView):
    template_name = 'blogs/index.html'
    context_object_name = 'latest_blog_list'
    paginate_by = 10
    def get_queryset(self):
        return Blog.objects.all().order_by('-pub_date')

# renders blog information
class DetailView(generic.DetailView):
    model = Blog
    template_name = 'blogs/detail.html'
    def get_queryset(self):
        return Blog.objects.all()

# only if user logged in
@login_required
# creates blog with BlogForm if everything is valid
def creation(request):
    if request.method =='POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            user_form = form.save(commit=False)
            user_form.user = request.user
            user_form.save()
            return redirect('blogs:index')
    # else rerenders page
    else:
        form = BlogForm()
    return render(request, 'blogs/creation.html', {'form': form})