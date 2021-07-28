from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import DeviceModel, NumberModel, ImageModel, Profile

from .forms import ProfileForm

import plotly.graph_objects as go
from plotly.offline import plot

import numpy as np

from pytz import timezone
import datetime

from django.utils import timezone
from django_pandas.io import read_frame

LIMIT_QUERY = getattr(settings, "LIMIT_QUERY", 10000)

def memefunc(request):
    host = settings.ALLOWED_HOSTS
    port = 8025#docker-compose.ymlで設定したmailhog_urlのHTTPポート

    mailhog_url = 'http://' + host[0] + ':' + str(port) + '/'

    return render(request, 'top.html', {'mailhog_url': mailhog_url})


@login_required
def readfunc(request):
    #ユーザーが登録したデータを取得
    username = request.user.get_username()
<<<<<<< HEAD
=======
    t =User.objects.filter(username__contains=username).values('last_name')
>>>>>>> def25fd97447de12832996abc177a3138cb443c3
    parameter = request.GET
    parameter_l = len(parameter)
    flag = False
    if parameter_l == 0:
        flag = True
    else:
        param_name = parameter['name']
        param_channel = parameter['channel']
<<<<<<< HEAD
        all_name = list(DeviceModel.objects.filter(user=request.user).distinct('name').values_list('name', flat=True))
        all_name.append('$all')
        all_channel = list(DeviceModel.objects.filter(user=request.user).distinct('channel').values_list('channel', flat=True))
        all_channel.append('$all')
        #all_device_id = list(DeviceModel.objects.filter(user=request.user).distinct('device_id').values_list('device_id', flat=True))
=======
        all_name = list(IotModel.objects.filter(long_id__contains=t).distinct('name').values_list('name', flat=True))
        all_name.append('$all')
        all_channel = list(IotModel.objects.filter(long_id__contains=t).distinct('channel').values_list('channel', flat=True))
        all_channel.append('$all')
>>>>>>> def25fd97447de12832996abc177a3138cb443c3
        not_known = not ((param_name in all_name) and (param_channel in all_channel))
        if not_known:
            flag = True
        else:
            if param_channel == '$all':
                if param_name == '$all':
                    flag = True
                else:
<<<<<<< HEAD
                    user_db = NumberModel.objects.filter(device__user=request.user, device__name=param_name).order_by('time').reverse().select_related().values('time', 'device__channel', 'device__name', 'data')[:LIMIT_QUERY]
            else:
                if param_name == '$all':
                    user_db = NumberModel.objects.filter(device__user=request.user, device__channel=param_channel).order_by('time').reverse().select_related().values('time', 'device__channel', 'device__name', 'data')[:LIMIT_QUERY]
                else:
                    user_db = NumberModel.objects.filter(device__user=request.user, device__name=param_name, device__channel=param_channel).order_by('time').reverse().select_related().values('time', 'device__channel', 'device__name', 'data')[:LIMIT_QUERY]
    if flag:
        user_db = NumberModel.objects.filter(device__user=request.user).order_by('time').reverse().select_related().values('time', 'device__channel', 'device__name', 'data')[:LIMIT_QUERY]
    
    df = read_frame(user_db)
    df_i = df.set_index('time')
    df['time'] = df_i.index.tz_convert('Asia/Tokyo')
    df = df.rename(columns={'device__channel': 'channel', 'device__name': 'name'})
    html_object = df.to_html(classes='table table-light table-striped table-hover table-bordered table-responsive')
    profile = Profile.objects.get(user=request.user)
    initial_data = {'alive_monitoring':profile.alive_monitoring,
                    'send_message_to_email':profile.send_message_to_email,
                    'line_token':profile.line_token,
                    'send_message_to_line':profile.send_message_to_line
                    }
    profile_form = ProfileForm(request.POST or None,initial=initial_data)
    return render(request, 'detail.html', {'table':html_object ,'username':username, "profile_form": profile_form})

=======
                    user_db = IotModel.objects.filter(long_id__contains=t, name=param_name).order_by('time').reverse()[:LIMIT_QUERY]
            else:
                if param_name == '$all':
                    user_db = IotModel.objects.filter(long_id__contains=t, channel=param_channel).order_by('time').reverse()[:LIMIT_QUERY]
                else:
                    user_db = IotModel.objects.filter(long_id__contains=t, name=param_name, channel=param_channel).order_by('time').reverse()[:LIMIT_QUERY]
    if flag:
        user_db = IotModel.objects.filter(long_id__contains=t).order_by('time').reverse()[:LIMIT_QUERY]
    
    df = read_frame(user_db, fieldnames=['time', 'channel', 'name', 'data'])
    df_i = df.set_index('time')
    df['time'] = df_i.index.tz_convert('Asia/Tokyo')
    html_object = df.to_html(classes='table table-light table-striped table-hover table-bordered table-responsive')
    return render(request, 'detail.html', {'table':html_object ,'username':username})
>>>>>>> def25fd97447de12832996abc177a3138cb443c3




@login_required
def graphfunc(request):
    #ユーザーが登録したデータを取得
    username = request.user.get_username()
<<<<<<< HEAD
=======
    t =User.objects.filter(username__contains=username).values('last_name')
>>>>>>> def25fd97447de12832996abc177a3138cb443c3
    parameter = request.GET
    parameter_l = len(parameter)

    ch_flag = False
    na_flag = False
    if parameter_l == 0:
        ch_flag = True
        na_flag = True
    else:
        param_name = parameter['name']
        param_channel = parameter['channel']
<<<<<<< HEAD
        all_name = list(DeviceModel.objects.filter(user=request.user).distinct('name').values_list('name', flat=True))
        all_name.append('$all')
        all_channel = list(DeviceModel.objects.filter(user=request.user).distinct('channel').values_list('channel', flat=True))
=======
        all_name = list(IotModel.objects.filter(long_id__contains=t).distinct('name').values_list('name', flat=True))
        all_name.append('$all')
        all_channel = list(IotModel.objects.filter(long_id__contains=t).distinct('channel').values_list('channel', flat=True))
>>>>>>> def25fd97447de12832996abc177a3138cb443c3
        all_channel.append('$all')
        not_known = not ((param_name in all_name) and (param_channel in all_channel))
        if not_known:
            ch_flag = True
            na_flag = True
        else:
            if param_channel == '$all':
                if param_name == '$all':
                    ch_flag = True
                    na_flag = True
                else:
                    ch_flag = True
                    na_flag = False
            else:
                if param_name == '$all':
                    ch_flag = False
                    na_flag = True
                else:
                    ch_flag = False
                    na_flag = False
    
    if ch_flag:
<<<<<<< HEAD
        channels = DeviceModel.objects.filter(user=request.user, data_type='number').distinct('channel').order_by('channel').values_list('channel', flat=True)
=======
        channels = IotModel.objects.filter(long_id__contains=t).filter(type='number').distinct('channel').order_by('channel').values_list('channel', flat=True)
>>>>>>> def25fd97447de12832996abc177a3138cb443c3
        channels_len = len(channels)
    else:
        channels = [param_channel]
        channels_len = 1
    
    plot_list = []
    for ch in channels:
        if na_flag:
<<<<<<< HEAD
            plot_db = NumberModel.objects.filter(device__user=request.user, device__data_type='number', device__channel=ch).order_by('time').reverse().select_related().values('time', 'device__name', 'data')[:LIMIT_QUERY//channels_len]
        else:
            plot_db = NumberModel.objects.filter(device__user=request.user, device__data_type='number', device__channel=ch, device__name=param_name).order_by('time').reverse().select_related().values('time', 'device__name', 'data')[:LIMIT_QUERY//channels_len]
        df = read_frame(plot_db)
        df_i = df.set_index('time')
        df['time'] = df_i.index.tz_convert('Asia/Tokyo')
        #データの形を整える
        device_name = df['device__name'] 
=======
            plot_db = IotModel.objects.filter(long_id__contains=t).filter(type='number', channel=ch).order_by('time').reverse()[:LIMIT_QUERY//channels_len]
        else:
            plot_db = IotModel.objects.filter(long_id__contains=t).filter(type='number', channel=ch, name=param_name).order_by('time').reverse()[:LIMIT_QUERY//channels_len]
        df = read_frame(plot_db, fieldnames=['time', 'name', 'data'])
        df_i = df.set_index('time')
        df['time'] = df_i.index.tz_convert('Asia/Tokyo')
        #データの形を整える
        device_name = df['name'] 
>>>>>>> def25fd97447de12832996abc177a3138cb443c3
        device_name_set = device_name.drop_duplicates()
        device_time = df['time']
        device_content = df['data']
        device_content_list = [device_content[device_name == i] for i in device_name_set]
        device_time_list = [device_time[device_name == i] for i in device_name_set]
        #グラフ描画
        fig = go.Figure()
        for c,j,n in zip(device_content_list , device_time_list , device_name_set):#デバイス毎にfor
            data_y = []
            data_x = []
            for y,x in zip(np.array(c),np.array(j).flatten()):
                #数値以外が登録されていた場合は無視
                try:
<<<<<<< HEAD
                    data_y.append(y)
=======
                    num = float(y)
                    data_y.append(num)
>>>>>>> def25fd97447de12832996abc177a3138cb443c3
                except:
                    pass
                else:
                    time = x
                    data_x.append(time)
            
            fig.add_trace(go.Scatter(x=data_x, y=data_y, mode='lines+markers',name=str(n)))
        
        fig.update_layout(title_text=ch, title_x=0.5)
        plot_fig = plot(fig, output_type='div', include_plotlyjs=False)
        channel_data = {'plot':plot_fig}
        plot_list.append(channel_data)
<<<<<<< HEAD
    profile = Profile.objects.get(user=request.user)
    initial_data = {'alive_monitoring':profile.alive_monitoring,
                    'send_message_to_email':profile.send_message_to_email,
                    'line_token':profile.line_token,
                    'send_message_to_line':profile.send_message_to_line
                    }
    profile_form = ProfileForm(request.POST or None,initial=initial_data)
    return render(request, 'graph.html', {'plot_gantt':plot_list ,'username':username, "profile_form": profile_form})
=======
    return render(request, 'graph.html', {'plot_gantt':plot_list ,'username':username})
>>>>>>> def25fd97447de12832996abc177a3138cb443c3
