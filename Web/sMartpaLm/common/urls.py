from django.urls import path, include
from . import views


app_name = 'common'

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.index, name='home'),
    path('login', views.login_sys, name='login'),
    path('menu_list/', views.menu_list, name='menu_list'),
    path('logout/', views.logout_sys, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('admin_palm/', include('admin_palm.urls'))
]