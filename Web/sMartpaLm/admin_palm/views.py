from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("농장 관리자 페이지")

def palm(request):
    return render(request, 'admin_palm/palm.html')