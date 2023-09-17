from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Profile
import random
import http.client
from django.conf import settings
import datetime
import pywhatkit # whatsup message send
from django.contrib import messages
from django.contrib.auth import authenticate, login
from . config import *

from twilio.rest import Client # for sms # pip install twilio

# Create your views here.

def home(request):
    return render(request,"account/home.html")

# send otp by msg91                                           # not working
# def send_otp(mobile, otp):
#     conn = http.client.HTTPSConnection("api.msg91.com")
#     authkey = settings.authkey
#     headers = {"content-type": "application/json"}
#     url = "https://control.msg91.com/api/v5/otp?mobile=&template_id="
#     conn.request("GET", url, headers=headers)
#     res = comm.getresponse()



# send otp by whats'app                                     # working
# def send_otp(mobile, otp):
#     hour = int(datetime.datetime.now().hour)
#     minute = int(datetime.datetime.now().minute)
#     minute +=1
#     number = f"+91{mobile}"
#     msg = f"Your otp is : {otp}"
#     pywhatkit.sendwhatmsg(number,msg,hour,minute)

# send otp by twilio                                         # working
# def send_otp(mobile, otp):
#     account_sid = ac_id
#     auth_token = auth_token
#     client = Client(account_sid, auth_token)

#     mobile="+917999253233"

#     message = client.messages \
#     .create(
#         body = f"Your OTP is : {otp}",
#         from_='+16183685218', # jo number aapko issue hua hai wo
#         to ='+917999253231', # kise send krna hai and both numbr should be varified from twilio # mobile
#         )
#     print(message.sid)
#     print("otp is sent")

def send_otp(mobile , otp):
    print("otp is sent")

def register(request):
    if request.method == "POST":
        uname = request.POST.get('uname')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')

        if len(mobile)!=10:
            messages.error(request,"Mobile number should be in 10 digit")
            return redirect('register')
        
        try:
            if User.objects.get(username=uname):
                messages.warning(request,"Username already taken")
                return redirect('register')
        except Exception as identifier:
            pass
        user = User(username = uname , first_name = name )

        otp = str(random.randint(1000,9999))
        profile = Profile(user = user , mobile = mobile, opt = otp)
        send_otp(mobile, otp)
        user.save()
        profile.save()
        messages.success(request,"Otp has been sent")
        request.session['mobile'] = mobile
        return redirect('otp')
    return render(request,"account/register.html")

def login_handle(request):
    if request.method == "POST":
        _mobile = request.POST.get('mobile')
        user_name = request.POST.get('uname')
        # mobile se filter ki koi user is number se exixt karta hai
        user = Profile.objects.filter(mobile = _mobile).first()
        if user is None:
            context = {
                'messages':"User not found",
                'class':'danger',
            }
            return render(request,"account/login.html",context)
        oTp = str(random.randint(1000,9999))
        print(oTp)
        user.opt = oTp
        user.save()
        send_otp(_mobile,oTp)
        request.session['mobile']= _mobile
        return redirect('login_otp')
    return render(request,"account/login.html")

def login_otp(request):
    _mobile = request.session['mobile']
    context = {
        'mobile':_mobile,
    }
    if request.method == "POST":
        otp = request.POST.get('otp')
        print(otp)
        profile = Profile.objects.filter(mobile = _mobile).first()
        print(profile.mobile)

        if otp == profile.opt:
            user = User.objects.get(id = profile.user.id)
            login(request,user)
            return redirect('home')
        else:
            print("wrong")
            context = {
                'mobile': _mobile,
            }
            messages.error(request,"Wrong Otp")
            return render(request,"account/login_otp.html",context)
    return render(request,"account/login_otp.html",context)

def otp(request):
    mobile = request.session['mobile']
    context = {
        'mobile':mobile
    }
    return render(request,"account/otp.html",context)