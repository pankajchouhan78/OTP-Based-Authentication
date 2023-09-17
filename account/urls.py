from django.urls import path
from .import views
urlpatterns = [
    path('',views.home,name="home"),
    path('register/',views.register,name="register"),
    path('login/',views.login_handle,name="login"),
    path('otp/',views.otp,name="otp"),
    path('login_otp/',views.login_otp,name="login_otp"),
]
