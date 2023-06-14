from django.urls import path
from . import views

app_name = 'common'

urlpatterns = [
    path('', views.index, name='smartpalm_index'),
    # path('', views.index, name='index'),
    path('welcome', views.welcome, name='welcome'),
    path('menu_list/', views.menu_list, name='menu_list'),
    path('login/', views.login_sys, name='login'),
    path('logout/', views.logout_sys, name='logout'),
    path('signup/', views.signup, name='signup'),
]