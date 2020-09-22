from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

# def allowed_users(allowed_roles = []):
#     def decorator(view_func):
#         def wrapper_func(request, *args, **kwargs):
#             group = None
#             print("HI")
#             if request.user.groups.exists():
#                 group = request.user.groups.all()[0].name
#                 print("HEY",group)
#             if group in allowed_roles:
#                 return view_func(request, *args, **kwargs)
#             else:
#                 return redirect('/logout')
#                 #return HttpResponse("You are not authorized to view this page")
#         return wrapper_func
#     return decorator

def allowed_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        print(group)
        if group == 'customer':
            return view_func(request,*args,**kwargs)
        elif group == 'admin':
            return redirect('/adminhome')
            #return redirect('/logout')
            #return HttpResponse("You are not authorized to view this page")
    return wrapper_func

