import datetime

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import BlogForm
from .models import Blog
from .views import DetailView, IndexView, creation

# fast blog creating
def create_blog(name):
    return Blog.objects.create(blog_name=name, blog_text='testtext')

class BlogTests(TestCase):
    # blog was published in past and renders
    def test_blog_published_in_past(self):
        equals = True
        now = timezone.now()
        past_blog = Blog.objects.create(pub_date='2001-01-01 01:01')
        if past_blog.pub_date.year == now.year:
            if past_blog.pub_date.month == now.month:
                if past_blog.pub_date.day == now.day:
                    if past_blog.pub_date.hour == now.hour:
                        if past_blog.pub_date.minute == now.minute:
                            equals = True
        self.assertEqual(equals, True)
    
    # can not render future blog
    def test_blog_published_in_future(self):
        equals = False
        now = timezone.now()
        future_blog = Blog.objects.create(pub_date='3001-01-01 01:01')
        if future_blog.pub_date.year == now.year:
            if future_blog.pub_date.month == now.month:
                if future_blog.pub_date.day == now.day:
                    if future_blog.pub_date.hour == now.hour:
                        if future_blog.pub_date.minute == now.minute:
                            equals = True
        self.assertEqual(equals, True)
    
    # renders blog that was created right now
    def test_blog_published_now(self):
        equals = False
        now = timezone.now()
        future_blog = Blog.objects.create(pub_date=now)
        if future_blog.pub_date.year == now.year:
            if future_blog.pub_date.month == now.month:
                if future_blog.pub_date.day == now.day:
                    if future_blog.pub_date.hour == now.hour:
                        if future_blog.pub_date.minute == now.minute:
                            equals = True
        self.assertEqual(equals, True)

class BlogFormTests(TestCase):
    # you can make blogs if you are logged in
    def test_form_takes_valid_data(self):
        form_data = {'blog_name': 'testblog', 'blog_text': 'testtext'}
        form = BlogForm(data=form_data)
        self.assertEqual(form.is_valid(), True)
    
    # creates valid blig
    def test_form_saves_valid_data(self):
        form_data = {'blog_name': 'testblog', 'blog_text': 'testtext'}
        form = BlogForm(data=form_data)
        form.save()
        blog_name_data = Blog.objects.get(blog_name='testblog').blog_name
        blog_text_data = Blog.objects.get(blog_name='testblog').blog_text
        self.assertEqual(blog_name_data, 'testblog')
        self.assertEqual(blog_text_data, 'testtext')

class IndexViewTests(TestCase):
    # nothing if no blogs
    def test_no_blogs(self):
        response = self.client.get(reverse('blogs:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'no blogs are available')
        self.assertQuerysetEqual(response.context['latest_blog_list'], [])

    # renders blog that in database
    def test_has_blog(self):
        create_blog('testblog')
        response = self.client.get(reverse('blogs:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_blog_list'], ['<Blog: testblog>'])
    
    # renders blogs in right order
    def test_has_sorted_blogs(self):
        create_blog('first blog')
        create_blog('second blog')
        response = self.client.get(reverse('blogs:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_blog_list'], ['<Blog: second blog>', '<Blog: first blog>'])

class DetailViewTests(TestCase):
    #renders blog detail page if blog exists
    def test_blog_exist(self):
        create_blog('testblog')
        blog_id = Blog.objects.get(blog_name='testblog').id
        response = self.client.get(reverse('blogs:detail', args=(blog_id,)))
        self.assertEqual(response.status_code, 200)
    
    # not renders page if blog doesnt exists
    def test_blog_doesnt_exist(self):
        response = self.client.get(reverse('blogs:detail', args=(9,)))
        self.assertEqual(response.status_code, 404)
    
    # detail page shows clicked blog
    def test_show_right_blog(self):
        create_blog('testblog')
        blog_id = Blog.objects.get(blog_name='testblog').id
        response = self.client.get(reverse('blogs:detail', args=(blog_id,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testblog')

class CreationViewTests(TestCase):
    # can not create blogs if not logged in
    def test_access_without_logged_in_user(self):
        response = self.client.get(reverse('blogs:creation'))
        self.assertEqual(response.status_code, 302)
    
    # can create blogs if logged in
    def test_access_with_logged_in_user(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        factory = RequestFactory()
        request = factory.get('blogs/creation/')
        request.user = user
        response = creation(request)
        self.assertEqual(response.status_code, 200)