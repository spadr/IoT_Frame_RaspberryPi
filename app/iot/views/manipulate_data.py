from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import IotModel

import datetime

from django_pandas.io import read_frame

import pandas as pd


@login_required
def dlfunc(request):
    try:
        username = request.user.get_username()
        t =User.objects.filter(username__contains=username).values('last_name')
        user_db = IotModel.objects.filter(long_id__contains=t)
        df = read_frame(user_db, fieldnames=['time', 'channel', 'name', 'data'])
        now_ts = int(datetime.datetime.now().timestamp())
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=['+ str(now_ts) +']mypage.csv'
        df_i = df.set_index('time')
        df['time'] = df_i.index.tz_convert('Asia/Tokyo').tz_localize(None)
        df.to_csv(path_or_buf=response,index=True)
        return response
    except:
        return redirect('login')


@login_required
def deletefunc(request):
    try:
        username = request.user.get_username()
        t =User.objects.filter(username__contains=username).values('last_name')
        user_db = IotModel.objects.filter(long_id__contains=t)
        user_db.delete()
        return redirect('read')
    except:
        return redirect('login')
