from django.shortcuts import render
from Utilities.mqtt_message import MosPub, MosSub
from django.http import JsonResponse
from django.http import HttpResponse
from .models import userPalms
from  django.views.generic.base import TemplateView
from  django.views.generic import ListView, DetailView

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

class palm_view(TemplateView):
    template_name = 'admin_palm/palm_base.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_list'] = ['userPalms']
        return context
class palm_list(ListView):
    model = userPalms

class palm(DetailView):
    model = userPalms