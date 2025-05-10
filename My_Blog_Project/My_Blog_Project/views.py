from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect

def Index(request):
    #redirect is for small general purposes, for hard control is HttpresponseRedirect
        #HttpresRedir returns 302(found & temporary redirect)
    return redirect(reverse('App_Blog:blog_list'))
    # return HttpResponseRedirect(reverse('App_Blog:blog_list'))
    


