from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user

from subprocess import Popen,PIPE

# user name
def system_resource_monitor(request):
    user = "team07"

    ps = Popen(['ps','aux'], stdout = PIPE)
    ps = ps.communicate()[0]
    grep = Popen(['grep',user], stdout = PIPE, stdin = PIPE)
    output = grep.communicate(ps)[0].decode("utf-8")
    output = output.split('\n')
    data= {'cpu':0.0,'memory':0.0}
    for x in output:
        info=list(filter(None,x.split(' ')))
        if(len(x)>1):
            data['cpu']+=float(info[2])
            data['memory']+=float(info[3])
    return redirect('/')