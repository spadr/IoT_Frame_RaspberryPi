from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.core import serializers
<<<<<<< HEAD
from django.db import transaction
=======
>>>>>>> def25fd97447de12832996abc177a3138cb443c3

from .models import DeviceModel, NumberModel, ImageModel

import secrets
import datetime
import json

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from django.utils import timezone
UTC = datetime.timezone(datetime.timedelta(hours=0), 'UTC')


<<<<<<< HEAD
class DeviceSetApi(APIView):
=======
class DataReceiveApi(APIView):
>>>>>>> def25fd97447de12832996abc177a3138cb443c3
    def get(self, request):
        now_timestamp = int(datetime.datetime.now().timestamp())
        response = {'time': now_timestamp}
        return Response(response, status=HTTP_200_OK)

    def post(self, request):
        now_timestamp = int(datetime.datetime.now().timestamp())
        if not request.user.is_authenticated:
                return Response(status=HTTP_401_UNAUTHORIZED)
        
        datas = json.loads(request.body)
<<<<<<< HEAD
        packet = datas['content']
        device_name = packet['name']
        device_channel = packet['channel']
        device_type = packet['type']
        device_min = int(packet['interval'])
        device_status = bool(packet['monitoring'])
=======
        access_key = datas['key']
        project_id = getattr(settings, 'PROJECT_ID')
        project_key =access_key[0:len(project_id)]
        content = datas['content']
        if secrets.compare_digest(project_key, project_id):#project_idでkeyの頭部分をチェック
            alluser_last_name = {i['last_name'] for i in User.objects.values('last_name')}
            if access_key in alluser_last_name:#どのユーザーかチェック
                for packet in content:
                    sensor_name = packet['name']
                    sensor_channel = packet['channel']
                    sensor_time = packet['time']
                    sensor_data = packet['data']
                    sensor_type = packet['type']
                    
                    #登録処理
                    IotModel.objects.create(long_id=str(access_key),
                                            name=str(sensor_name),
                                            time=timezone.localtime(datetime.datetime.fromtimestamp(int(sensor_time), UTC)),
                                            channel =str(sensor_channel),
                                            type =str(sensor_type),
                                            data=str(sensor_data))
                
                response = {'time': now_timestamp}
                return Response(response, status=HTTP_201_CREATED)#正常終了のレスポンス
            
            else:
                return Response(status=HTTP_401_UNAUTHORIZED)#該当ユーザー無しのレスポンス
>>>>>>> def25fd97447de12832996abc177a3138cb443c3
        
        try:
            device = DeviceModel.objects.filter(user=request.user, channel=device_channel, name=device_name).order_by('activity').reverse().select_related()[0]
            #device = DeviceModel.objects.get(user=request.user, channel=device_channel, name=device_name)
        except:
            device = DeviceModel.objects.create(user=request.user,
                                                token=secrets.token_hex()+str(now_timestamp),
                                                name=device_name,
                                                channel=device_channel,
                                                data_type=device_type,
                                                is_active=True,
                                                monitoring=device_status,
                                                interval=device_min,
                                                activity=timezone.localtime(datetime.datetime.fromtimestamp(now_timestamp, UTC))
                                                )
        else:
<<<<<<< HEAD
            #device.activity=timezone.localtime(datetime.datetime.fromtimestamp(now_timestamp, UTC))
            device.data_type=device_type
            device.is_active=True
            device.monitoring=device_status
            device.interval=device_min
            device.save()
        
        response = {'time': now_timestamp, 'device_token': device.token}
        return Response(response, status=HTTP_201_CREATED)#正常終了のレスポンス


class DataReceiveApi(APIView):
=======
            return Response(status=HTTP_401_UNAUTHORIZED)#project_idが一致しない場合のレスポンス



class DataSendApi(APIView):
>>>>>>> def25fd97447de12832996abc177a3138cb443c3
    def get(self, request):
        now_timestamp = int(datetime.datetime.now().timestamp())
        response = {'time': now_timestamp}
        return Response(response, status=HTTP_200_OK)
<<<<<<< HEAD

    def post(self, request):
        now_timestamp = int(datetime.datetime.now().timestamp())
=======
    
    def post(self, request):
>>>>>>> def25fd97447de12832996abc177a3138cb443c3
        if not request.user.is_authenticated:
                return Response(status=HTTP_401_UNAUTHORIZED)
        
        datas = json.loads(request.body)
<<<<<<< HEAD
        content = datas['content']
        for packet in content:
            device_token = packet['device_token']
            device_time = int(packet['time'])
            device_data = packet['data']
            
            device = DeviceModel.objects.get(user=request.user, token=device_token)
            device.activity = timezone.localtime(datetime.datetime.fromtimestamp(now_timestamp, UTC))
            #if device.is_active == False:
            #send line massege
            device.is_active = True
            device.save()

            #登録処理
            data_type=device.data_type
            if data_type == 'number':
                NumberModel.objects.create(device=device,
                                           time=timezone.localtime(datetime.datetime.fromtimestamp(device_time, UTC)),
                                           data=float(device_data)
                                        )
            
            elif data_type == 'image':
                pass
            
            elif data_type == 'boolean':
                pass
            
            elif data_type == 'string':
                pass
            
            elif data_type == 'array':
                pass
            
            else:
                pass
        
        
        response = {'time': now_timestamp}
        return Response(response, status=HTTP_201_CREATED)#正常終了のレスポンス



class DataSendApi(APIView):
    def get(self, request):
        now_timestamp = int(datetime.datetime.now().timestamp())
        response = {'time': now_timestamp}
        return Response(response, status=HTTP_200_OK)
    
    def post(self, request):
        if not request.user.is_authenticated:
                return Response(status=HTTP_401_UNAUTHORIZED)
=======
        access_key = datas['key']
        project_id = getattr(settings, 'PROJECT_ID')
        project_key =access_key[0:len(project_id)]

        if secrets.compare_digest(project_key, project_id):#project_idでkeyの頭部分をチェック
            alluser_last_name = {i['last_name'] for i in User.objects.values('last_name')}
            if access_key in alluser_last_name:#どのユーザーかチェック
                try:
                    sensor_name = datas['name']
                    sensor_channel = datas['channel']
                    sensor_lengh = int(datas['lengh']) + 1
                    queryset = IotModel.objects.filter(long_id=access_key, channel=sensor_channel, name=sensor_name).order_by('time').reverse()[:sensor_lengh]
                    res_query = serializers.serialize('json', queryset)
                except:
                   return Response(status=HTTP_404_NOT_FOUND)#該当データ無しのレスポンス
                else:
                    return HttpResponse(res_query, content_type="text/json-comment-filtered")#正常終了のレスポンス
            
            else:
                return Response(status=HTTP_401_UNAUTHORIZED)#該当ユーザー無しのレスポンス
>>>>>>> def25fd97447de12832996abc177a3138cb443c3
        
        datas = json.loads(request.body)
        try:
            device_token = datas['device_token']
            data_lengh = int(datas['lengh']) + 1
            queryset = NumberModel.objects.filter(device__user=request.user, device__token=device_token).order_by('time').reverse().select_related()[:data_lengh]
            res_query = serializers.serialize('json', queryset)
        except:
            return Response(status=HTTP_404_NOT_FOUND)#該当データ無しのレスポンス
        else:
<<<<<<< HEAD
            return HttpResponse(res_query, content_type="text/json-comment-filtered")#正常終了のレスポンス


@login_required
@transaction.atomic
=======
            return Response(status=HTTP_401_UNAUTHORIZED)#project_idが一致しない場合のレスポンス


@login_required
>>>>>>> def25fd97447de12832996abc177a3138cb443c3
def browserpostfunc(request):
    now_timestamp = int(datetime.datetime.now().timestamp())
    if request.method == "GET":#GETの処理
        return HttpResponse()
    
<<<<<<< HEAD
=======
    username = request.user.get_username()
    t = User.objects.filter(username__contains=username).values_list('last_name', flat=True)
>>>>>>> def25fd97447de12832996abc177a3138cb443c3
    if request.method == "POST":#POSTの処理
        device_name = request.POST['name']
        device_channel = request.POST['channel']
        device_value = request.POST['data']
<<<<<<< HEAD

        device = DeviceModel.objects.get(user=request.user, channel=device_channel, name=device_name)

        #登録処理
        NumberModel.objects.create(device=device,
                                   time=timezone.localtime(datetime.datetime.fromtimestamp(now_timestamp, UTC)),
                                   data=float(device_value)
                                   )
        
        return redirect(request.META['HTTP_REFERER'])
=======
        #登録処理
        IotModel.objects.create(long_id=str(t[0]),
                                name=str(device_name),
                                time=timezone.localtime(datetime.datetime.fromtimestamp(now_timestamp, UTC)),
                                channel=str(device_channel),
                                type =str('number'),
                                data=str(device_value)
                                )
        
        return redirect(request.META['HTTP_REFERER'])
>>>>>>> def25fd97447de12832996abc177a3138cb443c3
