from django.urls import path
from . import views

app_name = 'admin_palm'

urlpatterns = [
    path('<str:username>', views.admin_veiw, name='admin_palm'),
    path('admin_user/', views.admin_user, name='admin_user'),
    path('farm/', views.admin_farm, name='admin_farm'),
]