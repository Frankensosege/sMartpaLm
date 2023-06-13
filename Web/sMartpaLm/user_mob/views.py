from django.shortcuts import render
from Utilities.mqtt_message import MosPub, MosSub
from django.http import JsonResponse

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
        print(message)
        pub = MosPub('common')
        pub.bub_message(message)
        return JsonResponse({'result': 'success'})
    else:
        error = '요청경로가 올바르지 않습니다.'
        return JsonResponse({'error': error})