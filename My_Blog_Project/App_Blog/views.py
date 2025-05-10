from django.shortcuts import render,HttpResponseRedirect,redirect

from .models import Blog,Comment,Likes
from django.views.generic import ListView,CreateView,UpdateView,DetailView,TemplateView,DeleteView
from django.urls import reverse,reverse_lazy
import uuid

from django.utils.text import slugify
from django.contrib.auth.decorators import login_required
from .forms import CommentForm

# bellow imorts are for blog details view
from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog, Comment
from .forms import CommentForm

# For showing my blogs view
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

# Create your views here.


class MyBlogs(LoginRequiredMixin,TemplateView):
    template_name='App_Blog/my_blogs.html'



def blog_list(request):
    context={}
    return render(request,'App_Blog/blog_list.html',context=context)

class CreateBlog(CreateView):
    model=Blog
    template_name='App_Blog/create_blog.html'
    fields=['blog_title', 'blog_image', 'blog_content']
    
    def form_valid(self, form):
        blog_obj=form.save(commit=False)
        blog_obj.author=self.request.user
        title=blog_obj.blog_title
        # blog_obj.slug=title.replace(' ','-')+"-"+str(uuid.uuid4())[:8]
        blog_obj.slug = (
            slugify(title) + "-" + str(uuid.uuid4())[:8]
        )
        blog_obj.save()
        return redirect(reverse('index'))
        # Here, we would record the user's interest using the message
        # passed in form.cleaned_data['message']
        return super().form_valid(form)


class BlogList(ListView):
    context_object_name='blogs'
    model=Blog
    template_name='App_Blog/blog_list.html'
    queryset=Blog.objects.order_by('-publish_date')




@login_required
def blog_details(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    comment_form = CommentForm()
    already_liked=Likes.objects.filter(blog=blog,user=request.user)
    comments = blog.blog_comment.all()  
    
    liked=False
    if already_liked:
        liked=True
    
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)  
            comment.user = request.user
            comment.blog = blog
            comment.save()
            return redirect('App_Blog:blog_details', slug=slug)
    
    context = {
        'blog': blog,
        'comment_form': comment_form,
        'comments': comments,  
        'liked':liked,
    }
    return render(request, 'App_Blog/blog_details.html', context=context)

@login_required
def liked(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    user = request.user
    already_liked = Likes.objects.filter(blog=blog, user=user)
    
    if not already_liked.exists():
        liked_post = Likes(blog=blog, user=user)
        liked_post.save()
    
    return redirect(reverse('App_Blog:blog_details', kwargs={'slug': blog.slug}))

@login_required
def unliked(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    user = request.user
    already_liked = Likes.objects.filter(blog=blog, user=user)
    already_liked.delete()
    
    return redirect(reverse('App_Blog:blog_details', kwargs={'slug': blog.slug}))


class UpdateBlogs(LoginRequiredMixin,UpdateView):
    model=Blog
    fields=('blog_title', 'blog_image', 'blog_content')
    template_name='App_Blog/edit_blog.html'
    
    def get_success_url(self):
        return reverse_lazy('App_Blog:blog_details',kwargs={'slug':self.object.slug})
