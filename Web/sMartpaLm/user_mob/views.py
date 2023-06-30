from django.shortcuts import render
from Utilities.mqtt_message import bub_message
from django.http import JsonResponse
from django.http import HttpResponse
from common.models import Farm, FarmPlant, Disease, SensorData
import paho.mqtt.publish as publish
import time

#MQTT 브로커에 연결되었을 때 호출되는 콜백 함수
def send_mqtt_message(topic, message):
    start_request = time.time()
    while True:
        if time.time() - start_request >= 5:
            break
        else:
            broker_address = "16.170.241.38"  # Mosquitto 브로커 IP 주소
            publish.single(topic, message, hostname=broker_address)
            time.sleep(1)

def mqtt_mosquitto(request, context=None):
    if request.method == 'POST':
        farm = request.POST.get('farm')
        if 'back' in request.POST:
            return palm_view(request)
        elif 'on_button' in request.POST:
            send_mqtt_message('led/control','on')
        elif 'off_button' in request.POST:
            send_mqtt_message('led/control','off')
    return render(request, 'user_mob/mqtt_pub_mos.html', context)

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
            'username': username,
            'farm_list': farm_list,
            'palm_context': palm_context
        }
    else:
        context['username'] = username
        context['farm_list'] = farm_list
        context['palm_context'] = palm_context
    if 'control-palm' in request.POST:
        context['farm'] = request.POST.get('farm')
        return mqtt_mosquitto(request,context)
        # return render(request, 'user_mob/mqtt_pub_mos.html', context)
    return render(request, 'palm_base.html', context)



# Create your views here.
def add_context(context=None, key=None, value=None):
    if context:
        context[key] = value
    else:
        context={
            key:value,
        }
    return context




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

