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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import math
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
Pkl_Filename = './models/rf_model3.sav'
with open(Pkl_Filename,'rb') as f:
    reloadModel = pickle.load(f,encoding='latin1')


@unauthenticated_user
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/home')
        else:
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
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('/signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('/signup')
            else:
                user = User.objects.create_user(username=username, password = password1, email = email, first_name = first_name, last_name = last_name)
                user.save()
                group = Group.objects.get(name = 'customer')
                user.groups.add(group)
                auth.login(request,user)
                return redirect('/home')

        else:
            messages.info(request,'password not matchedUsername Taken')
            return redirect('/signup')
    else:
        return render(request,'signup.html')


@login_required(login_url='/login')
def logout(request):
    auth.logout(request)
    return redirect('/login')


# Added by Prasanna
@login_required(login_url='/login')
def fileupload(request):
    return render(request,'fileupload.html')

@login_required(login_url='/login')
def input(request):
    return render(request,'input.html')



@login_required(login_url='/login')
@customers_only
def home(request):
    return render(request,'index.html')

def customerhome(request):
    return render(request,'index.html')


@login_required(login_url='/login')
def profile(request):
    return render(request,'profile.html')


@login_required(login_url='/login')
def about(request):
    return render(request,'about.html')


@login_required(login_url='/login')
def predict(request):
    if request.method == 'POST':
        temp = {}
        building_id = request.POST.get('building_id')
        meter_type = request.POST.get('meter_type')
        if meter_type:
            meter_type = meter_type.lower()

        date_in = request.POST.get('timestamp')
        if date_in:
            date_out = datetime(*[int(v) for v in date_in.replace('T', '-').replace(':', '-').split('-')])
            month = date_out.month
        else:
            month = None

        temp['air_temperature'] = request.POST.get('air_temperature')
        temp['cloud_coverage'] = request.POST.get('cloud_coverage')
        temp['dew_temperature'] = request.POST.get('dew_temperature')
        temp['precip_depth_1_hr'] = request.POST.get('precip_depth')
        temp['sea_level_pressure'] = request.POST.get('sea_level_pressure')
        primary_use = request.POST.get('primary_use')
        if primary_use:
            primary_use = primary_use.lower()
        temp['wind_speed'] = request.POST.get('wind_speed')
        temp['wind_direction'] = request.POST.get('wind_direction')
        temp['square_feet'] = request.POST.get('building_size')
        temp['year_built'] = request.POST.get('year_built')
        temp['floor_count'] = request.POST.get('floor_count')

        if not temp['cloud_coverage']:
            temp['cloud_coverage'] = 0
        if not temp['precip_depth_1_hr']:
            temp['precip_depth_1_hr'] = 0
        if not temp['dew_temperature']:
            temp['dew_temperature'] = 7.5
        if not temp['sea_level_pressure']:
            temp['sea_level_pressure'] = 1015.7
        if not temp['wind_direction']:
            temp['wind_direction'] = 178.0
        if not temp['wind_speed']:
            temp['wind_speed'] = 3.6
        

        temp['meter is 0'] = 0
        temp['meter is 1'] = 0
        temp['meter is 2'] = 0
        temp['meter is other'] = 0
        temp['meter is N/A'] = 0
        if(meter_type == 'electricity'):
            temp['meter is 0'] = 1
        elif(meter_type == 'chilledwater'):
            temp['meter is 1'] = 1
        elif(meter_type == 'steam'):
            temp['meter is 2'] = 1
        elif(meter_type == 'na' or meter_type == 'n/a'):
            temp['meter is N/A'] = 1
        else:
            temp['meter is other'] = 1


        temp['primary_use is Education'] = 0
        temp['primary_use is Office'] = 0
        temp['primary_use is Lodging/residential'] = 0
        temp['primary_use is Entertainment/public assembly'] = 0
        temp['primary_use is Public services'] = 0
        temp['primary_use is Parking'] = 0
        temp['primary_use is Healthcare'] = 0
        temp['primary_use is Retail'] = 0
        temp['primary_use is Manufacturing/industrial'] = 0
        temp['primary_use is Warehouse/storage'] = 0
        temp['primary_use is Other'] = 0
        temp['primary_use is Technology/science'] = 0
        temp['primary_use is Utility'] = 0
        temp['primary_use is Food sales and service'] = 0
        temp['primary_use is Religious worship'] = 0
        temp['primary_use is N/A'] = 0
        temp['primary_use is other'] = 0

        if(primary_use == 'education'):
            temp['primary_use is Education'] = 1
        if(primary_use == 'office'):
            temp['primary_use is Office'] = 1
        elif(primary_use == 'lodging/residential'):
            temp['primary_use is Lodging/residential'] = 1
        elif(primary_use == 'entertainment/public assembly'):
            temp['primary_use is Entertainment/public assembly'] = 1
        elif(primary_use == 'public services'):
            temp['primary_use is Public services'] = 1
        elif(primary_use == 'parking'):
            temp['primary_use is Parking'] = 1
        elif(primary_use == 'healthcare'):
            temp['primary_use is Healthcare'] = 1
        elif(primary_use == 'retail'):
            temp['primary_use is Retail'] = 1
        elif(primary_use == 'manufacturing/industrial'):
            temp['primary_use is Manufacturing/industrial'] = 1
        elif (primary_use == 'warehouse/storage'):
            temp['primary_use is Warehouse/storage'] = 1
        elif(primary_use == 'other'):
            temp['primary_use is Other'] = 1
        elif(primary_use == 'technology/science'):
            temp['primary_use is Technology/science'] = 1
        elif(primary_use == 'utility'):
            temp['primary_use is Utility'] = 1
        elif(primary_use == 'food sales and service'):
            temp['primary_use is Food sales and service'] = 1
        elif(primary_use == 'religious worship'):
            temp['primary_use is Religious worship'] = 1
        elif(primary_use == 'na' or primary_use == 'n/a'):
            temp['primary_use is N/A'] = 1
        else:
            temp['primary_use is other'] = 1

        
        temp['timestamp_parsed_month is 1'] = 0
        temp['timestamp_parsed_month is 3'] = 0
        temp['timestamp_parsed_month is 4'] = 0
        temp['timestamp_parsed_month is 5'] = 0
        temp['timestamp_parsed_month is 6'] = 0
        temp['timestamp_parsed_month is 7'] = 0
        temp['timestamp_parsed_month is 8'] = 0
        temp['timestamp_parsed_month is 9'] = 0
        temp['timestamp_parsed_month is 10'] = 0
        temp['timestamp_parsed_month is 11'] = 0
        temp['timestamp_parsed_month is 12'] = 0
        temp['timestamp_parsed_month is N/A'] = 0
        temp['timestamp_parsed_month is other'] = 0
        if (month == 1):
            temp['timestamp_parsed_month is 1'] = 1
        elif (month == 3):
            temp['timestamp_parsed_month is 3'] = 1
        elif (month == 4):
            temp['timestamp_parsed_month is 4'] = 1
        elif (month == 5):
            temp['timestamp_parsed_month is 5'] = 1
        elif (month == 6):
            temp['timestamp_parsed_month is 6'] = 1
        elif (month == 7):
            temp['timestamp_parsed_month is 7'] = 1
        elif (month == 8):
            temp['timestamp_parsed_month is 8'] = 1
        elif (month == 9):
            temp['timestamp_parsed_month is 9'] = 1
        elif (month == 10):
            temp['timestamp_parsed_month is 10'] = 1
        elif (month == 11):
            temp['timestamp_parsed_month is 11'] = 1
        elif (month == 12):
            temp['timestamp_parsed_month is 12'] = 1
        elif (month == 2):
            temp['timestamp_parsed_month is other'] = 1
        else:
            temp['timestamp_parsed_month is N/A'] = 1
                
        testdata = pd.DataFrame({'x':temp}).transpose()
        scoreval = reloadModel.predict(testdata)[0]
        scoreval = round(scoreval,2)
        user = request.user
        obj = Energy_Data(username = user,
                        building_id = building_id,
                        air_temperature = temp['air_temperature'],
                        cloud_coverage = temp['cloud_coverage'],
                        dew_temperature = temp['dew_temperature'],
                        floor_count = temp['floor_count'],
                        precip_depth_1_hr = temp['precip_depth_1_hr'],
                        sea_level_pressure = temp['sea_level_pressure'],
                        building_size = temp['square_feet'],
                        wind_direction = temp['wind_direction'],
                        wind_speed = temp['wind_speed'],
                        year_built = temp['year_built'],
                        primary_use = primary_use,
                        timestamp = date_out,
                        meter_type = meter_type,
                        meter_reading = scoreval)
        obj.save()
        context = {'scoreval':scoreval}
        return render(request, 'input.html',context)
    else:
        redirect('/input')

@login_required(login_url='/login')
def uploadfile(request):
    if request.method=='POST' and len(request.FILES) == 1  and  request.FILES['datafile']:
        myfile = request.FILES['datafile']
        fs = FileSystemStorage()
        fname = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(fname)
        uploaded_file_url = os.path.join(os.getcwd(),fname)
        df = pd.read_csv(uploaded_file_url)
        total_cols=len(df.axes[1])
        global id_first
        global id_last
        id_first = -1
        id_last = -1
        with open(uploaded_file_url) as csv_file:
            csv_reader=csv.reader(csv_file,delimiter=',')
            numberOfRows=-1
            columns = []
            mapped = {}
            for row in csv_reader:
                if(numberOfRows == -1):
                    columns = row
                    for i in range(0,len(columns)):
                        mapped[row[i]] = i
                    numberOfRows = numberOfRows + 1
                    continue
                temp = {}
                if total_cols == 15:
                    building_id = row[mapped['Building Id']]
                    meter_type = row[mapped['Meter Type']]

                    if meter_type:
                        meter_type = meter_type.lower()

                    date_in = row[mapped['Timestamp']]
                    if date_in:
                        date_out = datetime.strptime(date_in,"%d-%m-%Y %H:%M")
                        month = date_out.month
                    else:
                        month = None

                    temp['air_temperature'] = row[mapped['Air Temperature']]
                    temp['cloud_coverage'] = row[mapped['Cloud Coverage']]
                    temp['dew_temperature'] = row[mapped['Dew Temperature']]
                    temp['precip_depth_1_hr'] = row[mapped['Precip Depth']]
                    temp['sea_level_pressure'] = row[mapped['Sea Level Pressure']]
                    primary_use = row[mapped['Primary Use']]
                    if primary_use:
                        primary_use = primary_use.lower()
                    temp['wind_speed'] = row[mapped['Wind Speed']]
                    temp['wind_direction'] = row[mapped['Wind Direction']]
                    temp['square_feet'] = row[mapped['Building Size']]
                    temp['year_built'] = row[mapped['Year Built']]
                    temp['floor_count'] = row[mapped['Floor Count']]

                elif total_cols == 14:
                    building_id = row[mapped['Building Id']]
                    meter_type = row[mapped['Meter Type']]

                    if meter_type:
                        meter_type = meter_type.lower()
                    

                    date_in = row[mapped['Timestamp']]
                    if date_in:
                        date_out = datetime.strptime(date_in,"%d-%m-%Y %H:%M")
                        month = date_out.month
                    else:
                        month = None

                    temp['air_temperature'] = row[mapped['Air Temperature']]
                    temp['cloud_coverage'] = row[mapped['Cloud Coverage']]
                    temp['dew_temperature'] = row[mapped['Dew Temperature']]
                    temp['precip_depth_1_hr'] = row[mapped['Precip Depth']]
                    temp['sea_level_pressure'] = row[mapped['Sea Level Pressure']]
                    primary_use = row[mapped['Primary Use']]
                    if primary_use:
                        primary_use = primary_use.lower()
                    temp['wind_speed'] = row[mapped['Wind Speed']]
                    temp['wind_direction'] = row[mapped['Wind Direction']]
                    temp['square_feet'] = row[mapped['Building Size']]
                    temp['year_built'] = row[mapped['Year Built']]
                    temp['floor_count'] = row[mapped['Floor Count']]

                if not temp['cloud_coverage']:
                    temp['cloud_coverage'] = 0
                if not temp['precip_depth_1_hr']:
                    temp['precip_depth_1_hr'] = 0
                if not temp['dew_temperature']:
                    temp['dew_temperature'] = 7.5
                if not temp['sea_level_pressure']:
                    temp['sea_level_pressure'] = 1015.7
                if not temp['wind_direction']:
                    temp['wind_direction'] = 178.0
                if not temp['wind_speed']:
                    temp['wind_speed'] = 3.6
                if not temp['floor_count']:
                    temp['floor_count'] = 2


                temp['meter is 0'] = 1
                temp['meter is 1'] = 0
                temp['meter is 2'] = 0
                temp['meter is other'] = 0
                temp['meter is N/A'] = 0

                if(meter_type == 'electricity'):
                    temp['meter is 0'] = 1
                elif(meter_type == 'chilledwater'):
                    temp['meter is 1'] = 1
                elif(meter_type == 'steam'):
                    temp['meter is 2'] = 1
                elif(meter_type == 'na' or meter_type == 'n/a'):
                    temp['meter is N/A'] = 1
                else:
                    temp['meter is other'] = 1

                temp['primary_use is Education'] = 0
                temp['primary_use is Office'] = 0
                temp['primary_use is Lodging/residential'] = 0
                temp['primary_use is Entertainment/public assembly'] = 0
                temp['primary_use is Public services'] = 0
                temp['primary_use is Parking'] = 0
                temp['primary_use is Healthcare'] = 0
                temp['primary_use is Retail'] = 0
                temp['primary_use is Manufacturing/industrial'] = 0
                temp['primary_use is Warehouse/storage'] = 0
                temp['primary_use is Other'] = 0
                temp['primary_use is Technology/science'] = 0
                temp['primary_use is Utility'] = 0
                temp['primary_use is Food sales and service'] = 0
                temp['primary_use is Religious worship'] = 0
                temp['primary_use is N/A'] = 0
                temp['primary_use is other'] = 0

                if(primary_use == 'education'):
                    temp['primary_use is Education'] = 1
                if(primary_use == 'office'):
                    temp['primary_use is Office'] = 1
                elif(primary_use == 'lodging/residential'):
                    temp['primary_use is Lodging/residential'] = 1
                elif(primary_use == 'entertainment/public assembly'):
                    temp['primary_use is Entertainment/public assembly'] = 1
                elif(primary_use == 'public services'):
                    temp['primary_use is Public services'] = 1
                elif(primary_use == 'parking'):
                    temp['primary_use is Parking'] = 1
                elif(primary_use == 'healthcare'):
                    temp['primary_use is Healthcare'] = 1
                elif(primary_use == 'retail'):
                    temp['primary_use is Retail'] = 1
                elif(primary_use == 'manufacturing/industrial'):
                    temp['primary_use is Manufacturing/industrial'] = 1
                elif (primary_use == 'warehouse/storage'):
                    temp['primary_use is Warehouse/storage'] = 1
                elif(primary_use == 'other'):
                    temp['primary_use is Other'] = 1
                elif(primary_use == 'technology/science'):
                    temp['primary_use is Technology/science'] = 1
                elif(primary_use == 'utility'):
                    temp['primary_use is Utility'] = 1
                elif(primary_use == 'food sales and service'):
                    temp['primary_use is Food sales and service'] = 1
                elif(primary_use == 'religious worship'):
                    temp['primary_use is Religious worship'] = 1
                elif(primary_use == 'na' or primary_use == 'n/a'):
                    temp['primary_use is N/A'] = 1
                else:
                    temp['primary_use is other'] = 1

                
                temp['timestamp_parsed_month is 1'] = 0
                temp['timestamp_parsed_month is 3'] = 0
                temp['timestamp_parsed_month is 4'] = 0
                temp['timestamp_parsed_month is 5'] = 0
                temp['timestamp_parsed_month is 6'] = 0
                temp['timestamp_parsed_month is 7'] = 0
                temp['timestamp_parsed_month is 8'] = 0
                temp['timestamp_parsed_month is 9'] = 0
                temp['timestamp_parsed_month is 10'] = 0
                temp['timestamp_parsed_month is 11'] = 0
                temp['timestamp_parsed_month is 12'] = 0
                temp['timestamp_parsed_month is N/A'] = 0
                temp['timestamp_parsed_month is other'] = 0
                if (month == 1):
                    temp['timestamp_parsed_month is 1'] = 1
                elif (month == 3):
                    temp['timestamp_parsed_month is 3'] = 1
                elif (month == 4):
                    temp['timestamp_parsed_month is 4'] = 1
                elif (month == 5):
                    temp['timestamp_parsed_month is 5'] = 1
                elif (month == 6):
                    temp['timestamp_parsed_month is 6'] = 1
                elif (month == 7):
                    temp['timestamp_parsed_month is 7'] = 1
                elif (month == 8):
                    temp['timestamp_parsed_month is 8'] = 1
                elif (month == 9):
                    temp['timestamp_parsed_month is 9'] = 1
                elif (month == 10):
                    temp['timestamp_parsed_month is 10'] = 1
                elif (month == 11):
                    temp['timestamp_parsed_month is 11'] = 1
                elif (month == 12):
                    temp['timestamp_parsed_month is 12'] = 1
                elif (month == 2):
                    temp['timestamp_parsed_month is other'] = 1
                else:
                    temp['timestamp_parsed_month is N/A'] = 1
                
                print(temp)
                testdata = pd.DataFrame({'x':temp}).transpose()
                scoreval = reloadModel.predict(testdata)[0]
                scoreval = round(scoreval,2)
                user = request.user

                obj = Energy_Data(username = user,
                                building_id = building_id,
                                air_temperature = temp['air_temperature'],
                                cloud_coverage = temp['cloud_coverage'],
                                dew_temperature = temp['dew_temperature'],
                                floor_count = temp['floor_count'],
                                precip_depth_1_hr = temp['precip_depth_1_hr'],
                                sea_level_pressure = temp['sea_level_pressure'],
                                building_size = temp['square_feet'],
                                wind_direction = temp['wind_direction'],
                                wind_speed = temp['wind_speed'],
                                year_built = temp['year_built'],
                                primary_use = primary_use,
                                timestamp = date_out,
                                meter_type = meter_type,
                                meter_reading = scoreval)

                obj.save()
                if(numberOfRows == 0):
                    id_first = obj.id
                numberOfRows= numberOfRows+1
        id_last = obj.id + numberOfRows
        fs.delete(fname)
        messages.success(request,'Please find the predictions and analyzed solutions below')
        return HttpResponse(reverse(fileupload))
    else:
        return redirect('/fileupload')

@login_required(login_url='/login')
def export_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename=MeterReading'  + '.csv'

    writer = csv.writer(response)
    writer.writerow(['SNo.',
                    'Building Id',
                    'Meter Type',
                    'Timestamp',
                    'Air Temperature',
                    'Cloud Coverage',
                    'Dew Temperature',
                    'Precip Depth for 1 hr',
                    'Sea Level Pressure',
                    'Primary Use',
                    'Wind Direction',
                    'Wind Speed',
                    'Building Size(sq feet)',
                    'Year Built',
                    'Floor Count',
                    'Meter Reading'])
    global id_first
    global id_last
    filtered_data = Energy_Data.objects.filter(id__range = [id_first,id_last])
    x = 1
    for data in filtered_data:
        writer.writerow([x,
                        data.building_id,
                        data.meter_type,
                        data.timestamp,
                        data.air_temperature,
                        data.cloud_coverage,
                        data.dew_temperature,
                        data.precip_depth_1_hr,
                        data.sea_level_pressure,
                        data.primary_use,
                        data.wind_direction,
                        data.wind_speed,
                        data.building_size,
                        data.year_built,
                        data.floor_count,
                        data.meter_reading])
        x = x + 1
    return response

@login_required(login_url='/login')
@admin_only
def adminhome(request):
    return render(request, 'adminhome.html')

@login_required(login_url='/login')
def adminfilter(request):
    meter_type = request.POST.get('meter_type')
    if meter_type:
        meter_type = meter_type.lower()
    meter_reading1 = request.POST.get('meter_reading1')
    meter_reading2 = request.POST.get('meter_reading2')

    timestamp1 = None
    timestamp2 = None
    date_in1 = request.POST.get('timestamp1')
    if date_in1:
        timestamp1 = datetime(*[int(v) for v in date_in1.replace('T', '-').replace(':', '-').split('-')])
    date_in2 = request.POST.get('timestamp2')
    if date_in2:
        timestamp2 = datetime(*[int(v) for v in date_in2.replace('T', '-').replace(':', '-').split('-')])

    primary_use = request.POST.get('primary_use')
    if primary_use:
        primary_use = primary_use.lower()
    year_built1 = request.POST.get('year_built1')
    year_built2 = request.POST.get('year_built2')
    building_size1 = request.POST.get('building_size1')
    building_size2 = request.POST.get('building_size2')
    floor_count1 = request.POST.get('floor_count1')
    floor_count2 = request.POST.get('floor_count2')
    wind_speed1 = request.POST.get('wind_speed1')
    wind_speed2 = request.POST.get('wind_speed2')
    wind_direction1 = request.POST.get('wind_direction1')
    wind_direction2 = request.POST.get('wind_direction2')
    cloud_coverage1 = request.POST.get('cloud_coverage1')
    cloud_coverage2 = request.POST.get('cloud_coverage2')
    air_temperature1 = request.POST.get('air_temperature1')
    air_temperature2 = request.POST.get('air_temperature2')
    dew_temperature1 = request.POST.get('dew_temperature1')
    dew_temperature2 = request.POST.get('dew_temperature2')
    precip_depth1 = request.POST.get('precip_depth1')
    precip_depth2 = request.POST.get('precip_depth2')
    sea_level_pressure1 = request.POST.get('sea_level_pressure1')
    sea_level_pressure2 = request.POST.get('sea_level_pressure2')

    filtered_data = Energy_Data.objects.all()
    if meter_type:
        filtered_data = filtered_data.filter(meter_type=meter_type)
    if meter_reading1 and meter_reading2:
        filtered_data = filtered_data.filter(meter_reading__range = [meter_reading1,meter_reading2])
    if timestamp1 and timestamp2:
        filtered_data = filtered_data.filter(timestamp__range = [timestamp1,timestamp2])
    if primary_use:
        filtered_data= filtered_data.filter(primary_use=primary_use)
    if year_built2 and year_built2:
        filtered_data = filtered_data.filter(year_built__range = [year_built1,year_built2])
    if building_size1 and building_size2:
        filtered_data = filtered_data.filter(building_size__range = [building_size1,building_size2])
    if floor_count1 and floor_count2:
        filtered_data = filtered_data.filter(floor_count__range = [floor_count1,floor_count2])
    if wind_speed1 and wind_speed2:
        filtered_data = filtered_data.filter(wind_speed__range = [wind_speed1, wind_speed2])
    if wind_direction1 and wind_direction2:
        filtered_data = filtered_data.filter(wind_direction__range = [wind_direction1, wind_direction2])
    if cloud_coverage1 and cloud_coverage2:
        filtered_data = filtered_data.filter(cloud_coverage__range = [cloud_coverage1, cloud_coverage2])
    if air_temperature1 and air_temperature2:
        filtered_data = filtered_data.filter(air_temperature__range = [air_temperature1,air_temperature2])
    if dew_temperature1 and dew_temperature2:
        filtered_data = filtered_data.filter(dew_temperature__range = [dew_temperature1,dew_temperature2])
    if precip_depth1 and precip_depth2:
        filtered_data = filtered_data.filter(precip_depth_1_hr__range = [precip_depth1,precip_depth2])
    if sea_level_pressure1 and sea_level_pressure2:
        filtered_data = filtered_data.filter(sea_level_pressure__range = [sea_level_pressure1, sea_level_pressure2])

    page = request.GET.get('page',1)
    paginator = Paginator(filtered_data, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request,'adminhome.html',{'users': users})


@login_required(login_url='/login')
@admin_only
def userdetails(request):
    user = get_user_model()
    user_data = user.objects.filter(is_superuser = False)
    page = request.GET.get('page',1)
    paginator = Paginator(user_data, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(10)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request,'userdetails.html',{'users':users})


@login_required(login_url='/login')
def password_changed(request):
  messages.success(request, 'Your password has been changed.')
  context = {'a':1}
  return render(request,'password_change_form.html',context)


@login_required(login_url='/login')
@admin_only
def admin_password_changed(request):
  messages.success(request, 'Your password has been changed.')
  context = {'a':1}
  return render(request,'admin_change_pwd.html',context)


@login_required(login_url='/login')
def clear_prediction(request):
    user_id = request.user.id
    Energy_Data.objects.filter(username = user_id).delete()
    return redirect('/insights')