from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User, auth

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def customers_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'customer':
            return view_func(request,*args,**kwargs)
        else:
            return redirect('/adminhome')
    return wrapper_func


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group != 'customer':
            return view_func(request,*args,**kwargs)
        else:
            return redirect('/home')
    return wrapper_func

