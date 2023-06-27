from django.shortcuts import render
from Utilities.mqtt_message import MosPub, MosSub
from django.http import JsonResponse
from django.http import HttpResponse
from common.models import Farm, FarmPlant, Disease, SensorData
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView

import config.settings as set

# Create your views here.
def mqtt_rabbit(request):
    return render(request, 'user_mob/mqtt_pub.html')

def mqtt_mosquitto(request):
    return render(request, 'user_mob/mqtt_pub_mos.html')

def mqtt_mossub(request):
    pass

def mqtt_mospub(request):
    if request.method == 'GET':
        message = request.GET.get('message')
        topic = request.GET.get('topic')
        print(message)
        mqc = MosPub(topic)
        mqc.bub_message(message)
        return JsonResponse({'result': 'success'})
    else:
        error = '요청경로가 올바르지 않습니다.'
        return JsonResponse({'error': error})

def mqtt_mossub(request):
    # print(set.STATICFILES_DIRS)
    if request.method == 'GET':
        topic = request.GET.get('topic')
        print(topic)
        # MosSub(topic)
        MosSub('#')
        # mqc.sub_message(topic)
        return JsonResponse({'result': 'success'})
    else:
        error = '요청경로가 올바르지 않습니다.'
        return JsonResponse({'error': error})

def mqtt_disconnect(request):
    pass


# Create your views here.

def index(request):
    return HttpResponse("농장관리자 페이지")


def palm_view(request, context=None):
    user = request.user
    palm_farms = Farm.objects.filter(user_id=user.id)
    farm_list = list(palm_farms)
    palm_context = {}
    for farm in farm_list:
        palm_values = FarmPlant.objects.filter(id=farm.id)
        if palm_values:
            palm_list = list(palm_values)
            palm_context[Farm.name] = palm_list
    print(palm_context)
    if not context:
        context = {
            'farm_list': farm_list,
            'palm_context': palm_context
        }
    else:
        context['farm_list'] = farm_list
        context['palm_context'] = palm_context
    return render(request, 'palm_base.html', context)