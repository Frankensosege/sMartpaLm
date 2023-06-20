from django.urls import path
from . import views

app_name = 'admin_palm'

urlpatterns = [
    path('', views.index, name='admin_palm'),
]