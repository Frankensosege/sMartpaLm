from django.shortcuts import render
from common.models import User

# Create your views here.

def index(request):
    admin_list = ["사용자 관리", "농장 관리", "모델 관리"]
    context_admin = {'admin_list': admin_list}
    palm_users = User.objects.all()
    user_list = list(palm_users)
    # palm_list = list(palm_users)
    # model_list = list(palm_users)
    context_user = {'user_list': user_list}

    combined_context = {**context_admin, **context_user}

    return render(request, 'admin_palm/palm.html', combined_context)
