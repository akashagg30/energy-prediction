"""interface URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from login import views,report,resources
from login.forms import EmailValidationOnForgotPassword

urlpatterns = [
    path('',views.login),
    path('signup',views.signup),
    # path('reset_password',views.reset_password),
    # ------------- user ------------------
    path('login',views.login),
    path('reset_password',auth_views.PasswordResetView.as_view(template_name = 'password_reset.html',form_class = EmailValidationOnForgotPassword), name="reset_password"),
    path('reset_password_sent',auth_views.PasswordResetDoneView.as_view(template_name = 'password_reset_sent.html'), name= "password_reset_done"),
    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name = 'password_reset_form.html'), name = "password_reset_confirm"),
    path('reset_password_complete',auth_views.PasswordResetCompleteView.as_view(template_name = 'password_reset_done.html'), name = "password_reset_complete"),
    path('change_password',auth_views.PasswordChangeView.as_view(template_name = 'password_change_form.html',success_url ='/password_changed'),name = 'password_change'),
    path('password_changed',views.password_changed),
    path('admin_change_pwd',auth_views.PasswordChangeView.as_view(template_name = 'admin_change_pwd.html',success_url ='/admin_password_changed'),name = 'password_change'),
    path('admin_password_changed',views.admin_password_changed),
    path('fileupload',views.fileupload),
    path('input', views.input),
    path('home', views.home),
    path('customerhome',views.customerhome),
    path('insights', report.Report),
    path('about', views.about),
    #----------
    path('logout',views.logout),
    path('profile',views.profile),
    path('predict',views.predict),
    path('adminhome',views.adminhome),
    path('userdetails',views.userdetails),
    path('exportcsv',views.export_csv),
    path('uploadfile',views.uploadfile),
    path('adminfilter',views.adminfilter),
    path('clear_prediction',views.clear_prediction),
    # ------------ system resource monitor --------
    path('resources',resources.system_resource_monitor),
    path('resources/get',resources.resource_info),
    # ------------- for fetching data realted to chatrs -------------
    path('insights/get',report.make_graph)
    ]
