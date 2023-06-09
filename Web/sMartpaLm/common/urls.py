from django.urls import path
from . import views

app_name = 'common'

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.smartpalm_index, name='smartpalm_index'),
]