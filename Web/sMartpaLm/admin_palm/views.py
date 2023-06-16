from django.shortcuts import render
from django.http import HttpResponse
from .models import userPalms
from  django.views.generic.base import TemplateView
from  django.views.generic import ListView, DetailView

# Create your views here.

def index(request):
    return HttpResponse("농장관리자 페이지")

class palm_view(TemplateView):
    template_name = 'admin_palm/palm.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_list'] = ['userPalms']
        return context
class palm_list(ListView):
    model = userPalms

class palm(DetailView):
    model = userPalms