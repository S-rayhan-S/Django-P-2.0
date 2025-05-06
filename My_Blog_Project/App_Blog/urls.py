from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required, permission_required


app_name='App_Blog'

urlpatterns = [
    path('',views.blog_list,name='blog_list'),
    path('write/',login_required(views.CreateBlog.as_view()),name='create_blog')
]








