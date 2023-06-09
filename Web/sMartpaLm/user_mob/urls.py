from django.urls import path
from . import views

app_name = 'user_mob'

urlpatterns = [
    path('mqtt_r/', views.mqtt_rabbit, name='mqtt_r'),
    path('mqtt_m/', views.mqtt_mosquitto, name='mqtt_m'),
    path('pub_m/', views.mqtt_mospub, name='pub_m'),
]