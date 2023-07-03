from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.http import HttpResponse
from Utilities.comUtilities import get_refresh_imgpath
from Utilities.mqtt_message import bub_message
import time, os
from common.models import Farm

def palm_view(request, username):
    user = request.user
    username = user.username

    return render(request, 'palm_base.html', {'username' : username})

def palm_list(request, username):
    user = request.user
    username = user.username
    farm_values = Farm.objects.filter(user_id=user.id)
    if farm_values:
        farm_list = list(farm_values)
        context = {
            'username' : username,
            'farm_list' : farm_list
        }
    else:
        context = {
            'username': username,
            'modified': '등록된 농장이 없습니다.'
        }
    return render(request, 'user_mob/palm_list.html',context)


def mqtt_mosquitto(request, username, farm, img_path=None):
    img_path = get_refresh_imgpath(username,farm)
    ref = {
        'ref' : 'refresh',
        'img_path': img_path,
           }
    context = {
        'username': username,
        'farm': farm,
        'ref' : ref,
    }
    topic_led = username+'/'+farm+'/LED'

    if request.method == 'POST':
        url = reverse('user_mob:mqtt_m', kwargs=context)
        if 'on_button' in request.POST:
            print(username+'/'+farm+'/LED')
            bub_message(topic_led, 'on')
            return redirect(url)
        elif 'off_button' in request.POST:
            bub_message(topic_led, 'off')
            return redirect(url)
        elif 'refresh' in request.POST:
            bub_message('refresh', 'refresh')
            time.sleep(5)
            return redirect(url)
    return render(request, 'user_mob/mqtt_pub_mos.html', context)


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

