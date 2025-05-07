from django.shortcuts import render,HttpResponseRedirect,redirect

from .models import Blog,Comment,Likes
from django.views.generic import ListView,CreateView,UpdateView,DetailView,TemplateView,DeleteView
from django.urls import reverse,reverse_lazy
import uuid
# Create your views here.
def blog_list(request):
    context={}
    return render(request,'App_Blog/blog_list.html',context=context)

class CreateBlog(CreateView):
    model=Blog
    template_name='App_Blog/create_blog.html'
    fields=['blog_title', 'blog_content']
    
    def form_valid(self, form):
        blog_obj=form.save(commit=False)
        blog_obj.author=self.request.user
        title=blog_obj.blog_title
        blog_obj.slug=title.replace(' ','-')+"-"+str(uuid.uuid4)
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








