from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user

from django.http import HttpResponse
from subprocess import Popen, PIPE
from json import dump
from django.views.decorators.csrf import csrf_protect


# user name


def system_resource_monitor(request):
    return render(request, 'resource_monitor.html', {
        'cpu': [cpu, 100.0-cpu],
        'memory': [memory, 100-memory]
    })

@csrf_protect
def resource_info(request):
    user = "team07"

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