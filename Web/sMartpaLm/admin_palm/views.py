from django.shortcuts import render
from common.models import User

# Create your views here.

def admin_veiw(request):
    admin_list = ["사용자 관리", "농장 관리", "모델 관리"]
    context_admin = {'admin_list': admin_list}
    return render(request, 'palm_base.html', context_admin)

def user_admin_view(request):
    palm_users = User.objects.all()
    user_list = list(palm_users)
    # palm_list = list(palm_users)
    # model_list = list(palm_users)
    context_user = {'user_list': user_list}
    print(user_list)
    return  render(request, 'admin_palm/admin_user.html', context_user)

