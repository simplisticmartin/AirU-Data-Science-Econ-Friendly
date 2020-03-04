from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
import json
# from .processing import *

tempB = ''

def home(request):
    context = {    
        'request' : request,   
        'lat_data': -34.397, 
        'lng_data': 150.644,

    }
    return render(request, 'home.html', context)

def data(request):
    if request.is_ajax():
        if request.method == 'POST':
            #listings,lon,lat,delta,tv,wifi,ac,kit,heating,roomtype,price,minutes
            listings = request.POST['listings']
            lat = request.POST['lat']
            lon = request.POST['lon']
            tv=request.POS['tv']
            wifi=request.POS['wifi']
            kitchen=request.POS['kitchen']
            ac=request.POS['ac']
            heat=request.POS['heating']
            roomtype=request.POS['roomtype']
            minutes=request.POS['time_max']
            price=request.POS['price_max']
            delta=0.002

            # same_community, B = get_A_B(listings,lon,lat,delta,tv,wifi,ac,kit,heating,roomtype,price,minutes)
            # tempB = B

            # print('Raw Data: "%s"' % same_community)
            # return same_community
    context = {    
        'request' : request,   
        'lat_data': -34.397, 
        'lng_data': 150.644,
    }
    return JsonResponse({'foo':'bar'})