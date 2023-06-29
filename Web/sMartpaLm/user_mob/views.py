from django.shortcuts import render, redirect
from Utilities.mqtt_message import bub_message
from django.http import JsonResponse
from django.http import HttpResponse
from common.models import Farm, FarmPlant, Disease, SensorData
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
import requests
import config.settings as set

#MQTT 브로커에 연결되었을 때 호출되는 콜백 함수

# Create your views here.
def mqtt_rabbit(request):
    pass
def mqtt_mosquitto(request, context=None):
    pass
    # if request.method == 'POST':
    #
    #     if 'on_button' in request.POST:
    #         led_control = 'on'
    #         on_led= True
    #           # "led/control" 토픽에 "on" 메시지 발행
    #     elif 'off_button' in request.POST:
    #         led_control = 'off'
    #         on_led = False # "led/control" 토픽에 "off" 메시지 발행
    #     elif 'refresh' in request.POST:
    #         refresh = 'picture'
    #              # on_message(client)
    # else:
    #     led_control = ''
    #     on_led = False
    #     refresh = ''# 임시 / 신호혹은 db데이터를 받는 부분
    # if context:
    #     context['led/control'] = str(led_control
    #     context['on_led'] = on_led
    #     context['refresh'] = refresh
    # else:
    #     context = {
    #         'led/control' : led_control,
    #         'on_led' : on_led,
    #         'refresh' : refresh,
    #     }
    # send_mqtt_message(context)
    # print(context)
    # return redirect('mqtt_m'.format(context))


def mqtt_mossub(request, data):
    return JsonResponse(data=data)

def mqtt_mospub(request):
    if request.method == 'GET':
        message = request.GET.get('message')
        topic = request.GET.get('topic')
        print(message)
        mqc = bub_message(topic, message)
        return JsonResponse({'result': 'success'})
    else:
        error = '요청경로가 올바르지 않습니다.'
        return JsonResponse({'error': error})
# def mqtt_mossub(request):
#     # print(set.STATICFILES_DIRS)
#     if request.method == 'GET':
#         topic = request.GET.get('topic')
#         print(topic)
#         # MosSub(topic)
#         MosSub('#')
#         # mqc.sub_message(topic)
#         return JsonResponse({'result': 'success'})
#     else:
#         error = '요청경로가 올바르지 않습니다.'
#         return JsonResponse({'error': error})



# def mqtt_disconnect(request):
#     pass


# Create your views here.

def index(request):
    return HttpResponse("농장관리자 페이지")

def palm_view(request, context=None):
    user = request.user
    username = user.username
    palm_farms = Farm.objects.filter(user_id=user.id)
    farm_list = list(palm_farms)
    palm_context = {}
    for farm in farm_list:
        palm_values = FarmPlant.objects.filter(id=farm.id)
        if palm_values:
            palm_list = list(palm_values)
            palm_context[Farm.name] = palm_list
    if not context:
        context = {
            'username':username,
            'farm_list': farm_list,
            'palm_context': palm_context
        }
    else:
        context['username'] = username
        context['farm_list'] = farm_list
        context['palm_context'] = palm_context
    if request.method == 'GET':
        if 'button-control' in request.GET:
            farmname = request.GET.get('button-control-text')
            context['farmname'] = farmname
            return mqtt_mosquitto(request, context)
    return render(request, 'palm_base.html', context)