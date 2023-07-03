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
