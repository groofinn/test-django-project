from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.core.paginator import Paginator
from .models import Author, Blog


class IndexView(generic.ListView):
    template_name = 'blogs/index.html'
    context_object_name = 'latest_blog_list'
    paginate_by = 2
    def get_queryset(self):
        return Blog.objects.all().order_by('-pub_date')

class DetailView(generic.DetailView):
    model = Blog
    template_name = 'blogs/detail.html'
    def get_queryset(self):
        return Blog.objects.all()

def reg(request):
    return render(request, 'blogs/reg.html', {Author.author_name: 'author_name'})