from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.http import HttpResponse
from Utilities.comUtilities import get_refresh_imgpath
from Utilities.mqtt_message import bub_message
import time, os
from common.models import Farm, SensoredData

def palm_view(request, username):
    user = request.user
    username = user.username

    return render(request, 'palm_base.html', {'username' : username})

def palm_list(request, username):
    user = request.user
    username = user.username
    row_data = SensoredData.objects.all()
    last_data = row_data.last()
    data = {
        # '조회 시각': last_data.timestamp,
        # '밝기(ch0)': round(last_data.ch0, 6),
        # '어둡기(ch1)': round(last_data.ch1, 6),
    }
    farm_values = Farm.objects.filter(user_id=user.id)
    if farm_values:
        farm_list = list(farm_values)
        context = {
            'username' : username,
            'farm_list' : farm_list,
            'data' : data,
        }
    else:
        context = {
            'username': username,
            'modified': '등록된 농장이 없습니다.'
        }
    return render(request, 'user_mob/palm_list.html', context)


def mqtt_mosquitto(request, username, farm):
    row_data = SensoredData.objects.all()
    last_data = row_data.last()
    img_path = 'data/images/'+username+'/'+farm+'/refresh.jpg'
    print(img_path)
    data = {
        # '조회 시각': last_data.timestamp,
        # '밝기(ch0)': round(last_data.ch0, 6),
        # '어둡기(ch1)': round(last_data.ch1, 6),
        # 조도 : round(last_data.light_amount, 6) * 'lux'
    }
    context = {
        'username': username,
        'farm': farm,
        'data': data,
        'img_path':img_path,
    }
    topic_led = username+'/'+farm+'/LED'
    if request.method == 'POST':
        # url = reverse('user_mob:mqtt_m', kwargs=context, )
        if 'on_button' in request.POST:
            print(username+'/'+farm+'/LED')
            bub_message(topic_led, 'on')
            # return render(request, 'user_mob/mqtt_pub_mos.html', context)
        elif 'off_button' in request.POST:
            bub_message(topic_led, 'off')
            # return render(request, 'user_mob/mqtt_pub_mos.html', context)
        elif 'refresh' in request.POST:
            bub_message('refresh', 'refresh')
            time.sleep(5)
            # return render(request, 'user_mob/mqtt_pub_mos.html', context)
        elif 'back' in request.POST:
            farm_values = Farm.objects.filter(user_id=request.user.id)
            if farm_values:
                farm_list = list(farm_values)
            context['farm_list'] = farm_list
            return render(request, 'user_mob/palm_list.html', context)
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

def index(request):
    return HttpResponse("농장관리자 페이지")

