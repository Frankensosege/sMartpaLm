from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm, UserCreationForm
from admin_palm.views import admin_veiw as adpalm
from user_mob.views import palm_view
import json
import paho.mqtt.client as mqtt
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SensorData

# MQTT Broker 설정
MQTT_BROKER = "16.170.241.38"
MQTT_PORT = 1883
MQTT_TOPIC = "test/farm1/sensored_data"
@csrf_exempt
def receive_mqtt_message(payload):
    message = json.loads(payload)
    
    timestamp = message['date']
    ch0 = message['ch0']
    ch1 = message['ch1']
    
    sensor_data = SensorData(timestamp=timestamp, ch0=ch0, ch1=ch1)
    sensor_data.save()
    
    return HttpResponse('OK')

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT Broker")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8')
    response = receive_mqtt_message(payload)
    print(response)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT)

client.loop_start()


def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return adpalm(request)
        else:
            return redirect('user_mob:user_palm')
    else:
        return redirect(request, 'common:login')

# views.py
def login_sys(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user=user)
            # redirect the user to the home page
            request.session['email'] = user.email
            request.session['id'] = user.id
            username = user.username
            if username is None or username == "":
                username = user.email
            request.session['username'] = username
            if user.is_superuser or user.is_staff:
                request.session['auth'] = 'A'
                user_format = {'user' : user}
                return redirect('admin_palm:admin_palm'.format(user_format))
            else:
                user_format = {'user': user}
                return redirect('user_mob:user_palm'.format(user_format))
            # redirect_to = reverse('login:welcome', kwargs={'name':user.username})
        else:
            # display an error message
            messages.error(request, '유효한 사용자가 아닙니다.')
            form = UserForm()
    else:
        form = UserForm()

    # render the login page
    return render(request, 'common/login.html', {'form': form})

def logout_sys(request):
    logout(request)
    if request.session.get('email'):
        del(request.session['email'])
        del(request.session['auth'])
        del(request.session['username'])
    return render(request, 'common/login.html')

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)

            login(request, user)
            return index(request)
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

def welcome(request):
    user = request.session.get('email')

    return render(request, 'common/sMartpaLm_index.html', {'user': user})