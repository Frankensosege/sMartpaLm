from django.urls import path
from . import views

app_name = 'user_mob'

urlpatterns = [
    path('mqtt_r/', views.mqtt_rabbit, name='mqtt_r'),
    path('mqtt_m/', views.mqtt_mosquitto, name='mqtt_m'),
    path('pub_m/', views.mqtt_mospub, name='pub_m'),
    path('sub_m/', views.mqtt_mossub, name='sub_m'),
    path('mqtt_disc/', views.mqtt_disconnect, name='mqtt_disc'),
    path('', views.palm_view.as_view(), name='sMartpaLm'),
    path('userPalms/', views.palm_list.as_view(), name='userPalms'),
    path('userPalms/Palm<int:pk>/', views.palm.as_view(), name='Palm'),
]
