from django.urls import path
from . import views

app_name = 'admin_palm'

urlpatterns = [
    path('<str:username>/', views.admin_veiw, name='admin_palm'),
]