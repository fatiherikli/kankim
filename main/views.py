# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login as _login, logout as _logout

from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from accounts.models import UserProfile, COLOR_CHOICES
from accounts.utils import me
from forms import RegistrationForm
from main.forms import LoginForm, ProfileEditForm, ProfilePictureForm


def index(request):
    if request.user.is_anonymous():
        return HttpResponseRedirect("/register")
    else:
        return home(request)


def home(request):
    ctx = {}
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/")


    friend_requests = me(request).friendship_requests()
    ctx["friendship_requests"]=friend_requests
    

    return render_to_response("home.html", context_instance = RequestContext(request, ctx))


def login(request):
    login_form = LoginForm()
    if request.method == "POST":
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)
            _login(request, user)
            return HttpResponseRedirect("/")
 
        
    ctx = {
        "login_form" : login_form
    }
    return render_to_response("login.html", context_instance=RequestContext(request, ctx) )

def profile(request, username):
    user = get_object_or_404(User, username = username)
    ctx = {
        "profile" : user.get_profile()
    }
    return render_to_response("profile.html", context_instance=RequestContext(request, ctx) )

def register(request):
    registration_form = RegistrationForm()
    login_form = LoginForm()

    if request.method == "POST":
        registration_form = RegistrationForm(request.POST)

        if registration_form.is_valid():
            registration_form.save()

    ctx = {
        "registration_form" : registration_form,
        "login_form" : login_form,
        "color_choices" : COLOR_CHOICES,
    }
    return render_to_response("register.html", context_instance=RequestContext(request, ctx) )


def profile_edit(request):
    profile_form = ProfileEditForm(instance = me(request))
    if request.method == "POST":
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=me(request))
        if profile_form.is_valid():
            profile_form.save()

    ctx = {
        "profile_form" : profile_form,
        "color_choices" : COLOR_CHOICES,

    }
    return render_to_response("profile_edit.html", context_instance=RequestContext(request, ctx) )


def change_profile_picture(request):
    profile_form = ProfilePictureForm(instance = me(request))
    if request.method == "POST":
        #raise Exception(request.FILES['picture'])
        profile_form = ProfilePictureForm(request.POST, request.FILES, instance=me(request))
        if profile_form.is_valid():
            profile_form.save()

    ctx = {
        "profile_form" : profile_form,

    }
    return render_to_response("change_profile_picture.html", context_instance=RequestContext(request, ctx) )




def logout(request):
    _logout(request)
    return HttpResponseRedirect("/")
