from django.shortcuts import render, redirect, get_object_or_404
from common.models import User
from .forms import AdminUserForm
import json

# Create your views here.

def admin_veiw(request):
    admin_list = ["사용자 관리", "농장 관리", "모델 관리"]
    context = {
        'admin_list': admin_list
    }
    return render(request, 'palm_base.html', context)

def user_admin(request, user_id):
    palm_users = User.objects.all()
    user_list = list(palm_users)
    obj = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = AdminUserForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
    else:
        form = AdminUserForm(instance=obj)
    context = {
        'user_list': user_list,
        'form': form
    }

    return render(request, 'admin_palm/admin_user.html', context)

from django.http import JsonResponse

def update_row(request, row_id):
    # Retrieve the row from the database
    row = YourModel.objects.get(pk=row_id)

    # Update the Boolean property
    row.boolean_property = not row.boolean_property
    row.save()

    # Return a JSON response indicating the success of the operation
    return JsonResponse({'success': True})

