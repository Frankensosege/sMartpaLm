from django.urls import path, include
from . import views


app_name = 'common'

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.index, name='home'),
    path('login/', views.login_sys, name='login'),
    path('logout/', views.logout_sys, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('admin_palm/<str:username>/', include('admin_palm.urls')),
    path('user_mob/<str:username>', include('user_mob.urls'))
]