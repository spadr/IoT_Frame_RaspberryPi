from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import IotModel

import datetime

from django_pandas.io import read_frame

import pandas as pd


@login_required
def consolefunc(request):
    username = request.user.get_username()
    if request.method == "GET":#GETの処理
        return render(request, 'console.html', {'username':username})
    
    if request.method == "POST":#POSTの処理
        device_name = request.POST['name']
        device_channel = request.POST['channel']
        mode = request.POST['mode']
        if mode == 'select':
            query_parameter = '?name=' + device_name + '&channel=' + device_channel
            return redirect(request.META['HTTP_REFERER'] + query_parameter)

        t =User.objects.filter(username=username).values('last_name')
        if device_channel =='$all':
            if device_name =='$all':
                user_db = IotModel.objects.filter(long_id__contains=t)
            else:
                user_db = IotModel.objects.filter(long_id__contains=t, name=device_name) 
        else:
            if device_name =='$all':
                user_db = IotModel.objects.filter(long_id__contains=t, channel=device_channel)
            else:
                user_db = IotModel.objects.filter(long_id__contains=t, name=device_name, channel=device_channel)
        
        if mode == 'download':
            df = read_frame(user_db, fieldnames=['time', 'channel', 'name', 'data'])
            now_ts = int(datetime.datetime.now().timestamp())
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=['+ str(now_ts) +']mypage.csv'
            df_i = df.set_index('time')
            df['time'] = df_i.index.tz_convert('Asia/Tokyo').tz_localize(None)
            df.to_csv(path_or_buf=response,index=True)
            return response
        
        elif mode == 'delete':
            user_db.delete()
            return redirect(request.META['HTTP_REFERER'])
        
        else:
            pass
        
