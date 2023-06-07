from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("내손바닥의 똑똑한 농장입니다.")
