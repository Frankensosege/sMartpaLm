from django.shortcuts import render, redirect, reverse
from Utilities.mqtt_message import bub_message
from django.http import JsonResponse
from django.http import HttpResponse
from Utilities.comUtilities import get_refresh_imgpath, get_context_palm
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

def mqtt_mosquitto(request, username, farm):
    if request.method == 'POST':
        username = request.user.username
        farm = request.POST.get('farm')
        context = {
            'username':username,
            'farm':farm,
        }
        url = reverse('user_mob:mqtt_m', kwargs=context)
        print(username, farm)
        # send_mqtt_message('refresh', 'picture')
        if 'back' in request.POST:
            return redirect('user_mob:user_mob')
        elif 'on_button' in request.POST:
            send_mqtt_message('led/control', 'on')
        elif 'off_button' in request.POST:
            send_mqtt_message('led/control', 'off')
        elif 'refresh' in request.POST:
            send_mqtt_message('refresh', 'picture')
            start = time.time()
            while True:
                if time.time() - start >= 5:
                    return render(request, 'user_mob/mqtt_pub_mos.html', context)
        return redirect(url)
    return render(request, 'user_mob/mqtt_pub_mos.html')
def palm_view(request, username, farm=None, context=None):
    if 'control-palm' in request.POST:
        username = request.user.username
        farm = request.POST.get('farm')
        context= {
            'farm': farm,
            'username':username,
        }
        print(context,'1111')
        url = reverse('user_mob:mqtt_m', kwargs=context)
        return redirect(url)
        # return render(request, 'user_mob/mqtt_pub_mos.html', context)
    return render(request, 'palm_base.html', context)

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

