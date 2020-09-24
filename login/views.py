from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, admin_only, customers_only
from .models import Energy_Data
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime

import csv
import pandas as pd
import pickle
import os
from datetime import datetime
from django.contrib.auth import get_user_model
from django.template.response import TemplateResponse
from django.urls import reverse
# Create your views here.

id_first = -1
id_last = -1
Pkl_Filename = './models/rf_model_final.sav'
with open(Pkl_Filename,'rb') as f:
    reloadModel = pickle.load(f,encoding='latin1')


@unauthenticated_user
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        print(password)
        user = auth.authenticate(username=username,password=password)
        print(user)
        if user is not None:
            auth.login(request,user)
            print('Login Done')
            return redirect('/home')
        else:
            print('Wrong')
            messages.info(request,'Invalid Credentials')
            return redirect('/')

    else:
        return render(request,'login.html')

@unauthenticated_user
def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        print(password1)
        print(password2)
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                print('Username taken')
                return redirect('/signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                print('Email taken')
                return redirect('/signup')
            else:
                user = User.objects.create_user(username=username, password = password1, email = email, first_name = first_name, last_name = last_name)
                user.save()
                group = Group.objects.get(name = 'customer')
                user.groups.add(group)
                messages.info(request,'User Created')
                print('user created')
                auth.login(request,user)
                return redirect('/home')

        else:
            messages.info(request,'password not matchedUsername Taken')
            print('password not matched')
            return redirect('/signup')
    else:
        return render(request,'signup.html')


@login_required(login_url='/login')
def logout(request):
    auth.logout(request)
    return redirect('/login')


# Added by Prasanna
@login_required(login_url='/login')
@customers_only
def fileupload(request):
    return render(request,'fileupload.html')

@login_required(login_url='/login')
@customers_only
def input(request):
    return render(request,'input.html')



@login_required(login_url='/login')
@customers_only
def home(request):
    return render(request,'index.html')


@login_required(login_url='/login')
@customers_only
def profile(request):
    return render(request,'profile.html')


@login_required(login_url='/login')
@customers_only
def about(request):
    return render(request,'about.html')


@login_required(login_url='/login')
@customers_only
def predict(request):
    if request.method == 'POST':
        temp = {}
        building_id = request.POST.get('building_id')
        temp['air_temperature'] = request.POST.get('air_temperature')
        temp['dew_temperature'] = request.POST.get('dew_temperature')
        temp['building_size'] = request.POST.get('building_size')
        temp['year_built'] = request.POST.get('year_built')
        temp['floor_count'] = request.POST.get('floor_count')
        primary_use = request.POST.get('primary_use')
        meter_type = request.POST.get('meter_type')
        if(meter_type == 'electricity'):
            temp['meter is 0'] = 1
            temp['meter is 1'] = 0
            temp['meter is 2'] = 0
            temp['meter is other'] = 0
        elif(meter_type == 'chilledwater'):
            temp['meter is 0'] = 0
            temp['meter is 1'] = 1
            temp['meter is 2'] = 0
            temp['meter is other'] = 0
        elif(meter_type == 'steam'):
            temp['meter is 0'] = 0
            temp['meter is 1'] = 0
            temp['meter is 2'] = 1
            temp['meter is other'] = 0
        else:
            temp['meter is 0'] = 0
            temp['meter is 1'] = 0
            temp['meter is 2'] = 0
            temp['meter is other'] = 1
        if(primary_use == 'Education'):
            temp['primary_use is Education'] = 1
            temp['primary_use is Lodging/residential'] = 0
            temp['primary_use is Entertainment'] = 0
            temp['primary_use is Other'] = 0
            temp['primary_use is Parking'] = 0
            temp['primary_use is Office'] = 0
            temp['primary_use is Public services'] = 0
            temp['primary_use is Utility'] = 0
            temp['primary_use is Healtcare'] = 0
            temp['primary_use is Retail'] = 0
        elif(primary_use == 'Lodging/residential'):
            temp['primary_use is Education'] = 0
            temp['primary_use is Lodging/residential'] = 1
            temp['primary_use is Entertainment'] = 0
            temp['primary_use is Other'] = 0
            temp['primary_use is Parking'] = 0
            temp['primary_use is Office'] = 0
            temp['primary_use is Public services'] = 0
            temp['primary_use is Utility'] = 0
            temp['primary_use is Healtcare'] = 0
            temp['primary_use is Retail'] = 0
        elif(primary_use == 'Entertainment/public assembly'):
            temp['primary_use is Education'] = 0
            temp['primary_use is Lodging/residential'] = 0
            temp['primary_use is Entertainment'] = 1
            temp['primary_use is Other'] = 0
            temp['primary_use is Parking'] = 0
            temp['primary_use is Office'] = 0
            temp['primary_use is Public services'] = 0
            temp['primary_use is Utility'] = 0
            temp['primary_use is Healtcare'] = 0
            temp['primary_use is Retail'] = 0
        elif(primary_use == 'Parking'):
            temp['primary_use is Education'] = 0
            temp['primary_use is Lodging/residential'] = 0
            temp['primary_use is Entertainment'] = 0
            temp['primary_use is Other'] = 0
            temp['primary_use is Parking'] = 1
            temp['primary_use is Office'] = 0
            temp['primary_use is Public services'] = 0
            temp['primary_use is Utility'] = 0
            temp['primary_use is Healtcare'] = 0
            temp['primary_use is Retail'] = 0
        elif(primary_use == 'Office'):
            temp['primary_use is Education'] = 0
            temp['primary_use is Lodging/residential'] = 0
            temp['primary_use is Entertainment'] = 0
            temp['primary_use is Other'] = 0
            temp['primary_use is Parking'] = 0
            temp['primary_use is Office'] = 1
            temp['primary_use is Public services'] = 0
            temp['primary_use is Utility'] = 0
            temp['primary_use is Healtcare'] = 0
            temp['primary_use is Retail'] = 0
        elif(primary_use == 'Public services'):
            temp['primary_use is Education'] = 0
            temp['primary_use is Lodging/residential'] = 0
            temp['primary_use is Entertainment'] = 0
            temp['primary_use is Other'] = 0
            temp['primary_use is Parking'] = 0
            temp['primary_use is Office'] = 0
            temp['primary_use is Public services'] = 1
            temp['primary_use is Utility'] = 0
            temp['primary_use is Healtcare'] = 0
            temp['primary_use is Retail'] = 0
        elif(primary_use == 'Utility'):
            temp['primary_use is Education'] = 0
            temp['primary_use is Lodging/residential'] = 0
            temp['primary_use is Entertainment'] = 0
            temp['primary_use is Other'] = 0
            temp['primary_use is Parking'] = 0
            temp['primary_use is Office'] = 0
            temp['primary_use is Public services'] = 0
            temp['primary_use is Utility'] = 1
            temp['primary_use is Healtcare'] = 0
            temp['primary_use is Retail'] = 0
        elif(primary_use == 'Healthcare'):
            temp['primary_use is Education'] = 0
            temp['primary_use is Lodging/residential'] = 0
            temp['primary_use is Entertainment'] = 0
            temp['primary_use is Other'] = 0
            temp['primary_use is Parking'] = 0
            temp['primary_use is Office'] = 0
            temp['primary_use is Public services'] = 0
            temp['primary_use is Utility'] = 0
            temp['primary_use is Healtcare'] = 1
            temp['primary_use is Retail'] = 0
        elif(primary_use == 'Retail'):
            temp['primary_use is Education'] = 0
            temp['primary_use is Lodging/residential'] = 0
            temp['primary_use is Entertainment'] = 0
            temp['primary_use is Other'] = 0
            temp['primary_use is Parking'] = 0
            temp['primary_use is Office'] = 0
            temp['primary_use is Public services'] = 0
            temp['primary_use is Utility'] = 0
            temp['primary_use is Healtcare'] = 0
            temp['primary_use is Retail'] = 1
        else:
            temp['primary_use is Education'] = 0
            temp['primary_use is Lodging/residential'] = 0
            temp['primary_use is Entertainment'] = 0
            temp['primary_use is Other'] = 1
            temp['primary_use is Parking'] = 0
            temp['primary_use is Office'] = 0
            temp['primary_use is Public services'] = 0
            temp['primary_use is Utility'] = 0
            temp['primary_use is Healtcare'] = 0
            temp['primary_use is Retail'] = 0
        
        temp['sea_level_pressure'] = request.POST.get('sea_level_pressure')
        date_in = request.POST.get('timestamp')
        date_out = datetime(*[int(v) for v in date_in.replace('T', '-').replace(':', '-').split('-')])
        print(date_out)
        temp['timestamp'] = date_out.strftime("%m/%d/%Y %H:%M:%S")
        print(temp)
        testdata = pd.DataFrame({'x':temp}).transpose()
        print("&&&&&&&&&&&&&&")
        scoreval = reloadModel.predict(testdata)[0]
        print("---------------")
        #scoreval = 1
        user = request.user
        print("****************")
        obj = Energy_Data(username = user,
                        air_temeprature=temp['air_temperature'],
                        dew_temperature=temp['dew_temperature'],
                        building_size=temp['building_size'],
                        year_built=temp['year_built'],
                        floor_count=temp['floor_count'],
                        primary_use=temp['primary_use'],
                        meter=temp['meter'],
                        sea_level_pressure=temp['sea_level_pressure'],
                        timestamp=temp['timestamp'],
                        meter_reading = scoreval)
        obj.save()
        context = {'scoreval':scoreval}
        print(temp)
        #return redirect('/input',context)
        return render(request, 'input.html',context)

@login_required(login_url='/login')
@customers_only
def uploadfile(request):
    if request.method=='POST' and len(request.FILES)>0 and request.FILES['datafile']:
        myfile = request.FILES['datafile']
        fs = FileSystemStorage()
        fname = fs.save(myfile.name, myfile)
        print(fname)
        uploaded_file_url = fs.url(fname)
        print("HI",uploaded_file_url)
        print(os.getcwd())
        uploaded_file_url = os.path.join(os.getcwd(),fname)
        print("HI",uploaded_file_url)
        df = pd.read_csv(uploaded_file_url)
        total_cols=len(df.axes[1])
        print(total_cols)
        with open(uploaded_file_url) as csv_file:
            csv_reader=csv.reader(csv_file,delimiter=',')
            next(csv_reader)
            numberOfRows=0
            for row in csv_reader:
                print(row)
                temp = {}
                if total_cols == 10:
                    temp['primary_use'] = row[1]
                    temp['meter_type'] = row[2]
                    temp['air_temperature'] = row[3]
                    temp['dew_temperature'] = row[4]
                    temp['building_size'] = row[5]
                    temp['year_built'] = row[6]
                    temp['floor_count'] = row[7]
                    temp['sea_level_pressure'] = row[8]
                    temp['timestamp'] = row[9]
                elif total_cols == 9:
                    temp['primary_use'] = row[0]
                    temp['meter_type'] = row[1]
                    temp['air_temperature'] = row[2]
                    temp['dew_temperature'] = row[3]
                    temp['building_size'] = row[4]
                    temp['year_built'] = row[5]
                    temp['floor_count'] = row[6]
                    temp['sea_level_pressure'] = row[7]
                    temp['timestamp'] = row[8]
                testdata = pd.DataFrame({'x':temp}).transpose()
                scoreval = reloadModel.predict(testdata)[0]
                #scoreval = 1
                user = request.user
                print("score",scoreval)
                obj = Energy_Data(username = user,
                        air_temeprature=temp['air_temperature'],
                        dew_temperature=temp['dew_temperature'],
                        building_size=temp['building_size'],
                        year_built=temp['year_built'],
                        floor_count=temp['floor_count'],
                        primary_use=temp['primary_use'],
                        meter_type=temp['meter_type'],
                        sea_level_pressure=temp['sea_level_pressure'],
                        timestamp=temp['timestamp'],
                        meter_reading = scoreval)
                obj.save()
                print("temp",temp)
                if(numberOfRows == 0):
                    global id_first
                    id_first = obj.id
                numberOfRows=numberOfRows+1
        global id_last
        id_last = obj.id + numberOfRows
        fs.delete(fname)
        messages.success(request,'File uploaded successful')
        context = {'a':1}
        print(context['a'])
        #return TemplateResponse(request,'fileupload.html',context)
        #return render(request, 'fileupload.html',{'a': 1,'aas':123})
        return HttpResponse(reverse(fileupload))
        #return redirect(fileupload)
    else:
        return redirect('/fileupload')
@login_required(login_url='/login')
@customers_only
def export_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename=MeterReading'  + '.csv'

    writer = csv.writer(response)
    writer.writerow(['SNo.','Air Temperature','Dew Temperature','Precip Depth','Building Size','Year Built','Floor_Count','Meter Reading'])

    global id_first
    global id_last
    filtered_data = Energy_Data.objects.filter(id__range = [id_first,id_last])
    print(id_first,id_last)
    id_first = -1
    id_second = -1
    print(filtered_data)
    x = 1
    for data in filtered_data:
        writer.writerow([x,
                        data.air_temeprature,
                        data.dew_temperature,
                        data.building_size,
                        data.year_built,
                        data.floor_count,
                        data.primary_use,
                        data.meter_type,
                        data.sea_level_pressure,
                        data.timestamp,
                        data.meter_reading])
        x = x + 1
    return response



@login_required(login_url='/login')
@admin_only
def adminhome(request):
    if request.method == 'POST':
        meter_reading = request.POST.get('meter_reading')
        year_built1 = request.POST.get('year_built1')
        year_built2 = request.POST.get('year_built2')
        building_size1 = request.POST.get('building_size1')
        building_size2 = request.POST.get('building_size2')
        floor_count1 = request.POST.get('floor_count1')
        floor_count2 = request.POST.get('floor_count2')
        air_temperature1 = request.POST.get('air_temperature1')
        air_temperature2 = request.POST.get('air_temperature2')
        dew_temperature1 = request.POST.get('dew_temperature1')
        dew_temperature2 = request.POST.get('dew_temperature2')
        precip_depth1 = request.POST.get('precip_depth1')
        precip_depth2 = request.POST.get('precip_depth2')

        print(meter_reading)
        print(year_built1," ",year_built2)
        print(building_size2," ",building_size2)
        print(floor_count1," ",floor_count2)
        print(air_temperature1," ",air_temperature2)
        print(dew_temperature1," ",dew_temperature2)
        print(precip_depth1," ",precip_depth2)
        #filtered_data = Energy_prediction_Data.objects.all()
        filtered_data = Energy_Data.objects.all()
        print(filtered_data)
        if meter_reading:
            filtered_data = filtered_data.filter(meter_reading=meter_reading)
        if year_built2 and year_built2:
            filtered_data = filtered_data.filter(year_built__range = [year_built1,year_built2])
        if building_size1 and building_size2:
            filtered_data = filtered_data.filter(building_size__range = [building_size1,building_size2])
        if floor_count1 and floor_count2:
            filtered_data = filtered_data.filter(floor_count__range = [floor_count1,floor_count2])
        if air_temperature1 and air_temperature2:
            filtered_data = filtered_data.filter(air_temeprature__range = [air_temperature1,air_temperature2])
        if dew_temperature1 and dew_temperature2:
            filtered_data = filtered_data.filter(dew_temperature__range = [dew_temperature1,dew_temperature2])
        if precip_depth1 and precip_depth2:
            filtered_data = filtered_data.filter(precip_depth__range = [precip_depth1,precip_depth2])
        print(filtered_data)
        #return render(request,'adminhome.html',{'filtered_data':filtered_data})
    else:
        return render(request, 'adminhome.html')


@login_required(login_url='/login')
@admin_only
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required(login_url='/login')
@admin_only
def userdetails(request):
    user = get_user_model()
    user_data = user.objects.filter(is_superuser = False)
    print(user_data)
    return render(request,'userdetails.html',{'user_data':user_data})


@login_required
@customers_only
def password_changed(request):
  messages.success(request, 'Your password has been changed.')
  context = {'a' : 1}
  return render(request,'password_change_form.html',context)
    #return render(request,'password_reset.html')
# def reset_password_sent(request):
#     return render(request,'password_reset_sent.html')
