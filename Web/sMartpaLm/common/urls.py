from django.urls import path
from . import views

app_name = 'common'

urlpatterns = [
    # path('', views.index, name='index'),
    path('home/', views.welcome , name='home'),
    path('', views.login_sys, name='login'),
    path('menu_list/', views.menu_list, name='menu_list'),
    path('logout/', views.logout_sys, name='logout'),
    path('signup/', views.signup, name='signup'),
]