from django.urls import path
from . import views

app_name = 'admin_palm'

urlpatterns = [
    path('', views.admin_veiw, name='admin_palm'),
    path('user/', views.user_admin_view, name='admin_user'),
    path('farm/', views.user_admin_view, name='admin_farm'),
    path('model/', views.user_admin_view, name='admin_model'),
]