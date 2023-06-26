from django.urls import path
from . import views

app_name = 'admin_palm'

urlpatterns = [
    path('', views.admin_veiw, name='admin_palm'),
    path('admin_user/', views.admin_user, name='admin_user'),
    # path('admin_user/<int:user_id>/user', views.user_admin, name='admin_user_user'),
    # path('admin_user/<int:user_id>/superuser', views.user_admin, name='admin_user_superuser'),
    # path('farm/', views.user_admin_view, name='admin_farm'),
    # path('model/', views.user_admin_view, name='admin_model'),
]