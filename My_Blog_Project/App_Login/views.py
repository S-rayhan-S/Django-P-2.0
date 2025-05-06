from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import SignUpForm,UserProfileChange
from .forms import ProfilePic

# Create your views here.

def sign_up(request):
    form=SignUpForm()
    registered=False
    if request.method=='POST':
        form=SignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            registered=True
    context={
        'form':form,
        'registered':registered,
    }
    return render(request,'App_Login/signup.html',context=context)

def login_page(request):
    form=AuthenticationForm()
    if request.method=='POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(request,username=username,password=password)
            if user is not None :
                login(request,user)
                return redirect(reverse('index'))
    context={
        'form':form,
    }
    return render(request,'App_Login/login.html',context=context)


def logout_user(request):
    if not request.user.is_authenticated: 
        return redirect('index')
    logout(request)
    return redirect('index')

@login_required
def profile(request):
    return render(request,'App_Login/profile.html',context={})
    # return render(request,'App_Login/profile',context={})


@login_required
def user_change(request):
    current_user=request.user
    form=UserProfileChange(request.POST,instance=current_user)
    if request.method=='POST':
        form=UserProfileChange(request.POST,instance=current_user)
        if form.is_valid():
            form.save()
            form=UserProfileChange(instance=current_user)
    context={
        'form':form
    }
    return render(request,'App_Login/change_profile.html',context=context)

@login_required
def change_pass(request):
    current_user=request.user
    changed=False
    form=PasswordChangeForm(current_user,data=request.POST)
    if request.method=='POST':
        form=PasswordChangeForm(current_user,data=request.POST)
        if form.is_valid():
            form.save()
            changed=True
    context={
        'form':form,
        'changed':changed
    }
    return render(request,'App_Login/pass-change.html',context=context)

@login_required
def add_pro_pic(request):
    
    try:
        profile_pic=request.user.user_profile
        form=ProfilePic(instance=profile_pic)
    except:
        profile_pic=None
        form=ProfilePic()
        
    if request.method=='POST':
        if profile_pic:
            form=ProfilePic(request.POST, request.FILES,instance=profile_pic)
        else:
            form=ProfilePic(request.POST, request.FILES)
            
        if form.is_valid():
            user_obj=form.save(commit=False)
            user_obj.user=request.user
            user_obj.save()
            return redirect(reverse('App_Login:profile'))
    
    context={
        'form':form,
        'profile_pic_exists': profile_pic is not None
    }
    return render(request,'App_Login/pro_pic_add.html',context=context)