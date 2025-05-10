from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.decorators import login_required

app_name='App_Blog'

urlpatterns = [
    path('',views.BlogList.as_view(),name='blog_list'),
    path('write/',login_required(views.CreateBlog.as_view()),name='create_blog'),
    path('details/<slug:slug>',views.blog_details,name='blog_details'),
    path('liked/<pk>/',views.liked,name='liked_post'),
    path('unliked/<pk>/',views.unliked,name='unliked_post'),
    path('my-blogs/', login_required(views.MyBlogs.as_view()), name='my_blogs'), 
    path('edit/<pk>/',views.UpdateBlogs.as_view(),name='edit_blog') ,
    # path('my-blogs',views.MyBlogs.as_view(),name='my_blogs'),
]








