from django.urls import path
from . import views

app_name = 'common'

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.smartpalm_index, name='smartpalm_index'),
]