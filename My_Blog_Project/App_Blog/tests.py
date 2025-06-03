from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Blog, Comment, Likes
from .forms import CommentForm
import datetime
from django.utils import timezone



# Create your tests here.
class BlogModelTests(TestCase):
    def setUp(self):
        self.user=User.objects.create_user(
            username='demo_testuser',
            password='demo_pass_123'
        )
        self.blog=Blog.objects.create(
            author=self.user,
            blog_title='testing blog',
            slug='testing-blog-slug',
            blog_content='demo content lorem Ipsum ....',
            blog_image='blog_images/attention.png'
        )
    def test_blog(self):
            self.assertEqual(str(self.blog),'testing blog')
            self.assertEqual(self.blog.slug,'testing-blog-slug')
            self.assertEqual(self.blog.author.username,'demo_testuser')    
        
        
    def test_comment(self):
            comment=Comment.objects.create(
                blog=self.blog,
                user=self.user,
                comment="It's a test comment",     
            )
            self.assertEqual(str(comment), "It's a test comment")
            self.assertEqual(comment.blog, self.blog)    
    
    def test_like(self):
            like=Likes.objects.create(blog=self.blog, user=self.user)
            self.assertEqual(like.blog,self.blog)
            self.assertEqual(like.user,self.user)
        
    def test_timestamps(self):
        
        now = timezone.now()
        
        # Verify timestamps exist
        self.assertIsNotNone(self.blog.publish_date)
        self.assertIsNotNone(self.blog.update_date)
        
        # Verify timestamps are in the past or present
        self.assertLessEqual(self.blog.publish_date, now)
        self.assertLessEqual(self.blog.update_date, now)
        
        # Verify publish_date is before or equal to update_date
        self.assertLessEqual(self.blog.publish_date, self.blog.update_date)

class BlogViewTests(TestCase):
    def setUp(self):
        self.user=User.objects.create_user(
            username='demo_testuser',
            password='demo_pass_123'
        )
        self.blog=Blog.objects.create(
            author=self.user,
            blog_title='testing blog',
            slug='testing-blog-slug',
            blog_content='demo content lorem Ipsum ....',
            blog_image='blog_images/attention.png'
        )
        self.client.login(username='demo_testuser',
            password='demo_pass_123')
        
    def test_blog_list_view(self):
        response=self.client.get(reverse('App_Blog:blog_list'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, 'testing blog')
    
    def test_create_view(self):
        response=self.client.get(reverse('App_Blog:create_blog'))
        self.assertEqual(response.status_code,200)
        
    def test_blog_detail_view(self):
        response=self.client.get(
            reverse('App_Blog:blog_details', kwargs={
                'slug':self.blog.slug
            })
        )
        self.assertEqual(response.status_code,200)
        self.assertContains(response,'testing blog')


class CommentFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.blog = Blog.objects.create(
            author=self.user,
            blog_title='Test Blog',
            slug='test-blog',
            blog_content='Test content'
        )
        
    def test_coment_form_valdation(self):
        form_data={'comment':'test data content'}
        form=CommentForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_form(self):
        form_data={'comment':""}
        form=CommentForm(data=form_data)
        self.assertFalse(form.is_valid())







