import os
import io
import paho.mqtt.client as mqtt
from PIL import Image
from datetime import datetime

# MQTT broker 정보
broker_address = "16.170.241.38"
broker_port = 1883
image_data_topic = "farm1/image"
refresh_topic = "refresh"

# 이미지 저장 경로
image_folder = "./data/images"

# MQTT 클라이언트 초기화
client = mqtt.Client()

# MQTT 브로커에 연결되었을 때 호출되는 콜백 함수
def on_connect(client, userdata, flags, rc):
    print("MQTT broker 에 연결되었습니다.")
    client.subscribe(image_data_topic)
    client.subscribe(refresh_topic)

# MQTT 브로커로부터 메시지를 수신하였을 때 호출되는 콜백 함수
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

# MQTT 클라이언트에 연결 및 콜백 함수 설정
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, broker_port, 60)

# MQTT 메시지 수신을 위한 루프 실행
client.loop_forever()
