import json
import time
import datetime
import numpy as np

# 날짜, 시간 관련 문자열 형식
FORMAT_DATE = "%Y%m%d"
FORMAT_DATETIME = "%Y%m%d%H%M%S"
propFile = './config.ini'

import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import os, io
from PIL import Image
from datetime import datetime as dt

broker_address = "16.170.241.38"
broker_port = 1883
image_data_topic = "farm1/image"
refresh_topic = "refresh"
image_folder = '../ras_pictures'

client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message
client.connect(broker_address, broker_port, 60)

def on_connect(client, userdata, flags, rc):
    print("MQTT broker 에 연결되었습니다.")
    client.subscribe(image_data_topic)
    client.subscribe(refresh_topic)

def on_message(client, userdata, msg):
    try:
        if msg.topic == refresh_topic:
            # refresh topic인 경우
            image_data = msg.payload
            image = Image.open(io.BytesIO(image_data))
            filename = os.path.join(image_folder, "refresh.jpg")

        elif msg.topic == image_data_topic:
            # 기타 topic인 경우
            # 수신한 메시지의 페이로드를 이미지로 변환
            image_data = msg.payload
            image = Image.open(io.BytesIO(image_data))

            # 현재 시간을 파일명에 포함하여 이미지를 파일로 저장
            current_time = datetime.now().strftime("%Y-%m-%d %H-%M")
            filename = os.path.join(image_folder, "{}.jpg".format(current_time))
            image.save(filename)
            print("Received and saved image: " + filename)

    except Exception as e:
        print("Error during image processing: " + str(e))

def send_mqtt_message(topic, message):
    broker_address = "16.170.241.38"  # Mosquitto 브로커 IP 주소
    publish.single(topic, message, hostname=broker_address)


def get_property(propSection, propName):
    #property 파일에서 property 읽어오기
    import configparser as parser

    properties = parser.ConfigParser()
    properties.read(propFile, "utf-8")
    propertiesSection = properties[propSection]

    return propertiesSection[propName]

def get_today_str():
    today = datetime.datetime.combine(
        datetime.date.today(), datetime.datetime.min.time())
    today_str = today.strftime('%Y%m%d')
    return today_str


def get_time_str():
    return datetime.datetime.fromtimestamp(
        int(time.time())).strftime(FORMAT_DATETIME)
