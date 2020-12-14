from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from django.http import HttpResponse
from subprocess import Popen, PIPE
from json import dump
from django.views.decorators.csrf import csrf_protect
from .decorators import admin_only
import os
import pwd


# user name

@login_required(login_url='/login')
@admin_only
@csrf_protect
def system_resource_monitor(request):
    return render(request, 'resource_monitor.html')

@login_required(login_url='/login')
@admin_only
@csrf_protect
def resource_info(request):
    user = pwd.getpwuid(os.geteuid()).pw_name
    # user = "ghost38o"
    ps = Popen(['ps', 'aux'], stdout=PIPE)
    ps = ps.communicate()[0]
    grep = Popen(['grep', user], stdout=PIPE, stdin=PIPE)
    output = grep.communicate(ps)[0].decode("utf-8")
    output = output.split('\n')
    cpu = 0.0
    memory = 0.0
    for x in output:
        info = list(filter(None, x.split(' ')))
        if(len(x) > 1):
            cpu += float(info[2])
            memory += float(info[3])
    return HttpResponse(str(cpu)+" "+str(memory))
