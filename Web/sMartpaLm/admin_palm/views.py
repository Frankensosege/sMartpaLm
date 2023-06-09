from django.contrib.auth import authenticate
from django.shortcuts import render, redirect, get_object_or_404
from common.models import User, Farm
from .forms import AdminUserForm, AdminFarmForm
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
import json

# Create your views here.

def admin_veiw(request, username=None ,context=None):
    username = request.user.username
    palm_users = User.objects.all().order_by('id')
    user_list = list(palm_users)
    context = {
        'username': username,
        'user_list': user_list,
    }
    if request.method == 'POST':
        if 'admin_user' in request.POST:
            email = request.POST.get('email')
            is_active = request.POST.get('is_active')
            if email != "smartpalm@smartpalm.com":
                if is_active:
                    is_active = True
                else:
                    is_active = False
                is_superuser = request.POST.get('is_superuser')
                if is_superuser:
                    is_superuser = True
                else:
                    is_superuser = False

                user_row = get_object_or_404(User, email=email)
                user_row.is_active = is_active
                user_row.is_superuser = is_superuser
                user_row.save()
                context['username']= request.user.username
                context['modified']= user_row.email + '님의 사용자 권한이 변경되었습니다'
            else:
                context['username']=request.user.username
                context['modified']= 'Error : ' + email + '님은 관리자 입니다.'
        elif 'button-add' in request.POST:
            user_id = request.POST.get('user_id')
            name = request.POST.get('name')
            print('추가')
            form = AdminFarmForm(request.POST)
            user_row = get_object_or_404(User, id=user_id)
            if not Farm.objects.filter(name=name).exists():
                if form.is_valid():
                    farm = form.save(commit=False)
                    farm.name = name
                    farm.user = user_row
                    farm.save()
                    context['modified'] = user_row.username + '님의 농장이 추가 되었습니다.'
                else:
                    form = AdminFarmForm()
                    context['modified'] = 'Error : 농장명이 입력되지 않았습니다.'
                    context['form'] = form
            else:
                context['modified'] = 'Error : 농장명이 중복되었습니다.'
                context['form'] = form
        elif 'button-del' in request.POST:
            user_id = request.POST.get('user_id')
            name = request.POST.get('name')
            print('삭제')
            conditions = {'user_id': user_id, 'name': name}
            row_exists = Farm.objects.filter(**conditions).exists()
            if row_exists:
                del_row = Farm.objects.get(name=name)
                del_row.delete()
                context['modified'] = '농장 ' + name + '이 삭제되었습니다.'
            else:
                context['modified'] = '농장이 이미 존재하지 않습니다.'
    farm_context = {}
    for user in user_list:
        farm_values = Farm.objects.filter(user_id=user.id)
        if farm_values:
            farm_list = list(farm_values)
            farm_context[user.username] = farm_list
    context['farm_context']= farm_context
    return render(request, 'admin_base.html', context)
@require_POST
def admin_user(request):


    return admin_veiw(request, context=None)

def admin_farm(request):

    if request.method == 'POST':
        print('포스트')

    return render(request, 'admin_base.html', context)



