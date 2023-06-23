from django.contrib.auth import authenticate
from django.shortcuts import render, redirect, get_object_or_404
from common.models import User
from .forms import AdminUserForm
from django.http import HttpResponse
import json

# Create your views here.

def admin_veiw(request):
    palm_users = User.objects.all().order_by('id')
    user_list = list(palm_users)
    context = {
        'user_list': user_list
    }
    print(user_list)

    # if request.method == "POST":
    #     print(request.POST)
    #     form = AdminUserForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         email = form.cleaned_data.get('email')
    #         raw_password = form.cleaned_data.get('password1')
    #         user = authenticate(email=email, password=raw_password)
    #         login(request, user)
    #         return render(request, 'common/sMartpaLm_index.html')
    # else:
    #     form = UserForm()
    # # return render(request, 'common/signup.html', {'form': form})
    return render(request, 'palm_base.html', context)

def admin_user(request):
    if request.method == 'POST':
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
            print(user_row.is_active, user_row.is_superuser)
            user_row.is_active = is_active
            user_row.is_superuser = is_superuser
            user_row.save()
            print(user_row.is_active, user_row.is_superuser)
        else:
            palm_users = User.objects.all().order_by('id')
            user_list = list(palm_users)
            context = {
                'user_list': user_list,
                'modified': 'Error : ' + email + '님은 관리자 입니다.'
            }
            return render(request, 'palm_base.html', context)
    palm_users = User.objects.all().order_by('id')
    user_list = list(palm_users)
    context = {
        'user_list': user_list,
        'modified': user_row.email+'님의 사용자 권한이 변경되었습니다'
    }
    return render(request, 'palm_base.html', context)