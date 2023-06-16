from django.urls import path
from . import views

app_name = 'admin_palm'

urlpatterns = [
    path('', views.palm_view.as_view(), name='sMartpaLm'),
    path('userPalms/', views.palm_list.as_view(), name='userPalms'),
    path('userPalms/Palm<int:pk>/', views.palm.as_view(), name='Palm'),
]