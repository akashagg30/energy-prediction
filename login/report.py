from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user
from .models import *
from .decorators import unauthenticated_user, admin_only
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from login.models import Energy_Data as db
import numpy as np
# def extract


# sorts both teh lists according to order of first one
def sort_list(list1, list2):
    return (list(t) for t in zip(*sorted(zip(list1, list2))))


# calculating interquartile range
def IQR(data):
    Q1 = np.percentile(data, 25, interpolation='midpoint')
    Q2 = np.percentile(data, 75, interpolation='midpoint')
    return Q2-Q1


# for bar plot
def make_bins(X, Y):
    # temp data
    new_X = []
    new_Y = []
    n = 0
    sum = 0

    if len(X)==0:
        return (new_X,new_Y)

    X, Y = sort_list(X, Y)
    # calculating bin size
    h = int(2*IQR(X)*len(X)**(-1/3))
    left = min(X)
    right = left+h
    # generating bins
    for x, y in zip(X, Y):
        if x <= right:
            sum += y
            n += 1
        else:
            # appending values to list
            new_X.append(str(left)+"-"+str(right))
            new_Y.append(sum/n)
            # for next iteration
            sum = y
            n = 1
            left = right+1
            right = left+h

    if(n != 0):
        new_X.append(str(left)+"-"+str(right))
        new_Y.append(sum/n)

    return (new_X, new_Y)


# for line plot
def make_bars(X, Y):
    new_X = []
    new_Y = []
    
    if len(X)==0: return (new_X,new_Y)

    # dictionary having floors as key and [sum_of_electricity,count] as value for calculating mean
    floor = {}
    for x, y in zip(X, Y):
        if x not in floor:
            floor[x] = [0, 0]
        floor[x][0] += y
        floor[x][1] += 1
    for x in sorted(floor):
        new_X.append(x)
        new_Y.append(floor[x][0]/floor[x][1])
    return (new_X, new_Y)

@login_required(login_url='/login')
def Report(request):
    data = db.objects.filter(username=request.user.id).values()

    area=[]
    floorcount=[]
    age=[]
    temperature=[]
    electrictiy=[]

    for x in data:
        area.append(x['building_size'])
        floorcount.append(x['floor_count'])
        age.append(x['year_built'])
        temperature.append(x['air_temperature'])
        electrictiy.append(x['meter_reading'])

    # generating data for sending to charts to renger them
    X_Area_vs_electricity, Y_Area_vs_electricity = make_bins(area, electrictiy)
    X_Floorcount_vs_electricity, Y_Floorcount_vs_electricity = make_bars(
        floorcount, electrictiy)
    X_Temperature_vs_electricity, Y_Temperature_vs_electricity = make_bars(
        temperature, electrictiy)
    X_Age_vs_electricity, Y_Age_vs_electricity = make_bars(
        age, electrictiy)

    print(X_Temperature_vs_electricity)


    if request.user.is_authenticated:
        user_id = request.user.id
        # print(user_id)
        user_inputs = Energy_Data.objects.filter(username = user_id)
        page = request.GET.get('page',1)
        paginator = Paginator(user_inputs, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        # print(user_inputs)

    return render(request, 'insights.html', {
        'X_Area_vs_electricity': X_Area_vs_electricity,
        'Y_Area_vs_electricity': Y_Area_vs_electricity,

        'X_Floorcount_vs_electricity': X_Floorcount_vs_electricity,
        'Y_Floorcount_vs_electricity': Y_Floorcount_vs_electricity,

        'X_Temperature_vs_electricity': X_Temperature_vs_electricity,
        'Y_Temperature_vs_electricity': Y_Temperature_vs_electricity,

        'X_Age_vs_electricity': X_Age_vs_electricity,
        'Y_Age_vs_electricity': Y_Age_vs_electricity,

        'users':users
    })
