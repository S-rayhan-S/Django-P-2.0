from django.urls import path
from . import views

app_name='App_Login'
urlpatterns = [
    path('signup/',views.sign_up,name="signup"),
    path('login/',views.login_page,name="login"),
    path('logout/',views.logout_user,name="logout"),
    path('profile/',views.profile,name="profile"),
    path('change-profile',views.user_change,name='user-change'),
    path('password/',views.change_pass,name='pass-change'),
    path('add-picture/',views.add_pro_pic,name='add_pro_pic'),
    path('guest-login/', views.guest_login, name='guest_login'),    
]








