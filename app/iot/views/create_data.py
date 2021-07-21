from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.core import serializers

from .models import IotModel

import secrets
import datetime
import json

from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from django.utils import timezone
UTC = datetime.timezone(datetime.timedelta(hours=0), 'UTC')


class DataReceiveApi(APIView):
    def get(self, request):
        now_timestamp = int(datetime.datetime.now().timestamp())
        response = {'time': now_timestamp}
        return Response(response, status=HTTP_200_OK)

    def post(self, request):
        now_timestamp = int(datetime.datetime.now().timestamp())
        if not request.user.is_authenticated:
                return Response(status=HTTP_401_UNAUTHORIZED)
        
        datas = json.loads(request.body)
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
        
        else:
            return Response(status=HTTP_401_UNAUTHORIZED)#project_idが一致しない場合のレスポンス



class DataSendApi(APIView):
    def get(self, request):
        now_timestamp = int(datetime.datetime.now().timestamp())
        response = {'time': now_timestamp}
        return Response(response, status=HTTP_200_OK)
    
    def post(self, request):
        if not request.user.is_authenticated:
                return Response(status=HTTP_401_UNAUTHORIZED)
        
        datas = json.loads(request.body)
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
        
        else:
            return Response(status=HTTP_401_UNAUTHORIZED)#project_idが一致しない場合のレスポンス