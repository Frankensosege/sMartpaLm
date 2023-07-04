from django.urls import path, re_path
from . import views

app_name = 'user_mob'

urlpatterns = [
    path('<str:username>/', views.palm_view, name='user_mob'),
    path('palm_list/<str:username>/', views.palm_list, name='palm_list'),
    path('mqtt_m/<str:username>/<str:farm>/', views.mqtt_mosquitto, name='mqtt_m'),
    path('pub_m/', views.mqtt_mospub, name='pub_m'),
    path('sub_m/', views.mqtt_mossub, name='sub_m'),
    # path('mqtt_disc/', views.mqtt_disconnect, name='mqtt_disc'),

    # path('userPalms/Palm<int:pk>/', views.palm.as_view(), name='Palm'),
    # path('upload/', views.upload, name='upload'),
]
