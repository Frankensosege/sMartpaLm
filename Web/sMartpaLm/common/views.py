from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("내 손바닥 안에 똑똑한 농장입니다.")
