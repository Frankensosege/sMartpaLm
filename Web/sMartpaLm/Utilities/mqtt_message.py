# import paho.mqtt.client as mqtt
# import random
# from functools import wraps
# from Utilities.comUtilities import get_property
#
# def singleton(cls):
#     instances = {}
#     @wraps(cls)
#     def wrapper(*args, **kwargs):
#         if cls not in instances:
#             instances[cls] = cls(*args, **kwargs)
#         return instances[cls]
#     return wrapper
#
# @singleton
# class MQTTClient:
#     def __init__(self):
#         self.client = self.connect_mqtt()
#
#     def connect_mqtt(self):
#         # MQTT 클라이언트 생성 및 설정
#         client_id = f"mqtt_client_{random.randint(0, 1000)}"
#         client = mqtt.Client(client_id)
#         client.on_connect = self.on_connect
#         client.on_disconnect = self.on_disconnect
#         client.on_publish = self.on_publish
#         client.on_subscribe = self.on_subscribe
#         client.on_message = self.on_message
#         client.on_log = self.on_log
#
#         # MQTT 브로커에 연결
#         client.connect(get_property('URLs', 'mqtt_sever'), int(get_property('URLs', 'mqtt_port')), 60)
#
#         return client
#
#     def on_connect(self, client, userdata, flags, rc):
#         if rc == 0:
#             print("Connected to MQTT broker OK....")
#         else:
#             print("Failed to connect, result code:", rc)
#
#     def on_disconnect(self, client, userdata, flags, rc):
#         print("Disconnected result code:", rc)
#
#     def on_publish(self, client, userdata, mid):
#         print("In on_pub callback mid=", mid)
#
#     def on_subscribe(self, client, userdata, mid, granted_qos):
#         print("---------------- on_subscribe")
#         print("subscribed:", str(mid), str(granted_qos))
#
#     def on_message(self, client, userdata, msg):
#         print("---------------- on_message")
#         print(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")
#
#     def on_log(self, client, userdata, level, buf):
#         print(f"log: {buf}")
#
# @singleton
# class MosPub:
#     def __init__(self, topic):
#         self.topic = topic
#         self.client = MQTTClient().client
#
#     def bub_message(self, message):
#         self.client.loop_start()
#         msg = str(message)
#         result = self.client.publish(self.topic, msg)
#         self.client.loop_stop()
#
# @singleton
# class MosSub:
#     def __init__(self, topic):
#         self.topic = topic
#         self.client = MQTTClient().client
#         self.client.loop_forever()
#
#     def disconnect_sub(self):
#         self.client.disconnect()

# import random
# import paho.mqtt.client as mqtt
# from Utilities.comUtilities import get_property

# class MQTTClient:
#     connected_to_broker = False
#     def __new__(cls, *args, **kwargs):
#         if not hasattr(cls, "_instance"):
#             cls._instance = super().__new__(cls)
#         print("find created connection....")
#         return cls._instance
    
#     def __init__(self):
#         cls = type(self)
#         if not hasattr(cls, "_init"):
#             print("Start create connection....")
#             self.client = self.connect_mqtt()
#             cls._init = True

#     def __init__(self):
#         self.client = self.connect_mqtt()

#     def connect_mqtt(self):
#         def on_connect(client, userdata, flags, rc):
#             print('on_connect called!!!!!!!!')
#             # client.subscribe(self.topic)
#             if rc == 0:
#                 print("Connected to MQTT broker OK....")
#                 self.connected_to_broker = True
#             else:
#                 print("Failed to connect, result code : ", rc)

#         def on_disconnect(client, userdata, flags, rc=0):
#             print("Disconnected result code : ", str(rc))

#         def on_publish(client, userdata, mid):
#             print("In on_pub callback mid= ", mid)

#         def on_subscribe(client, userdata, mid, granted_qos):
#             print("---------------- on_subscribe")
#             print("subscribed: " + str(mid) + " " + str(granted_qos))

#         def on_message(client, userdata, msg):
#             print("---------------- on_messge")
#             print(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")

#         def on_log(client, userdata, level, buf):
#             print(f"log: {buf}")

#         print('connect to broker')
#         # 새로운 클라이언트 생성
#         client_id = f"mqtt_client_{random.randint(0, 1000)}"
#         client = mqtt.Client(client_id)

#         # 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속중료), on_publish(메세지 발행)
#         client.on_connect = on_connect
#         client.on_disconnect = on_disconnect
#         client.on_publish = on_publish
#         client.on_subscribe = on_subscribe
#         client.on_message = on_message
#         client.on_log = on_log

#         # address : localhost, port: 1883 에 연결
#         # self.client.connect('localhost', 1883)
#         client.connect(get_property('URLs', 'mqtt_sever'), int(get_property('URLs', 'mqtt_port')), 60)

#         return client

#     def bub_message(self, topic, message):
#         self.client.loop_start()
#         # topic 으로 메세지 발행
#         msg = f"messages: '{message}'"
#         result= self.client.publish(topic, msg)
#         self.client.loop_stop()
#         # 연결 종료
#         self.client.disconnect()

#     def sub_message(self, topic):
#         print('Waiting topic.....')
#         self.client.subscribe(self.topic)
#         self.client.loop_forever()
###############################################################

# class MosPub:
#     def __init__(self, topic):
#         self.topic = topic
#         self.client = self.connect_mqtt()

#     def connect_mqtt(self):
#         def on_connect(client, userdata, flags, rc):
#             if rc == 0:
#                 print("Connected to MQTT broker OK....")
#             else:
#                 print("Failed to connect, result code : ", rc)

#         def on_disconnect(client, userdata, flags, rc=0):
#             print("Disconnected result code : ", str(rc))

#         def on_publish(client, userdata, mid):
#             print("In on_pub callback mid= ", mid)

#         def on_log(client, userdata, level, buf):
#             print(f"log: {buf}")

#         # 새로운 클라이언트 생성
#         client_id = f"mqtt_client_{random.randint(0, 1000)}"
#         client = mqtt.Client(client_id)

#         # 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속중료), on_publish(메세지 발행)
#         client.on_connect = on_connect
#         client.on_disconnect = on_disconnect
#         client.on_publish = on_publish
#         client.on_log = on_log

#         # address : localhost, port: 1883 에 연결
#         # self.client.connect('localhost', 1883)
#         client.connect(get_property('URLs', 'mqtt_sever'), int(get_property('URLs', 'mqtt_port')))

#         return client

#     def bub_message(self, message):
#         self.client.loop_start()
#         # topic 으로 메세지 발행
#         msg = f"{message}"
#         result= self.client.publish(self.topic, msg)
#         self.client.loop_stop()
#         # 연결 종료
#         self.client.disconnect()

# class MosSub:
#     def __init__(self, topic):
#         self.topic = topic
#         self.client = self.connect_mqtt()
#         self.client.loop_forever()
#         # self.client.subscribe(self.topic)

#     def connect_mqtt(self):
#         def on_connect(client, userdata, flags, rc):
#             print("Connected with result code :", str(rc))
#             client.subscribe(self.topic)
#             # if rc == 0:
#             #     print("Connected to MQTT broker OK....")
#             # else:
#             #     print("Failed to connect, result code : ", rc)

#         def on_disconnect(client, userdata, flags, rc=0):
#             print("Disconnected result code : ", str(rc))

#         def on_subscribe(client, userdata, mid, granted_qos):
#             print("---------------- on_subscribe")
#             print("subscribed: " + str(mid) + " " + str(granted_qos))

#         def on_message(client, userdata, msg):
#             print("---------------- on_messge")
#             print(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")

#         def on_log(client, userdata, level, buf):
#             print(f"log: {buf}")

#         # 새로운 클라이언트 생성
#         client_id = f"mqtt_client_{random.randint(0, 1000)}"
#         client = mqtt.Client(client_id)

#         # 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속중료), on_publish(메세지 발행)
#         client.on_connect = on_connect
#         client.on_disconnect = on_disconnect
#         client.on_subscribe = on_subscribe
#         client.on_message = on_message
#         client.on_log = on_log

#         # address : localhost, port: 1883 에 연결
#         # self.client.connect('localhost', 1883)
#         client.connect(get_property('URLs', 'mqtt_sever'), int(get_property('URLs', 'mqtt_port')), 60)

#         return client

#     def disconnect_sub(self):
#         self.client.disconnect()

import random
import paho.mqtt.client as mqtt
from Utilities.comUtilities import get_property
from PIL import Image
import io, os
from datetime import datetime

def on_led(userId, farmid):
    topic = userId + '/' + farmid + '/LED/'
    bub_message(topic, 'on')

def refresh_img(userId, farmId):
    image_folder = get_property('DATA', 'base_dir') + get_property('DATA', 'imgpath')
    fileName = f"{userId}_{farmId}_refresh.jpg"

    if os.path.isfile(image_folder+fileName):
        os.remove(image_folder+fileName)

    topic = userId + '/' + farmId + '/refresh/'
    bub_message(topic, 'refresh')


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        print('on_connect called!!!!!!!!')
        # client.subscribe(self.topic)
        if rc == 0:
            print("Connected to MQTT broker OK....")
        else:
            print("Failed to connect, result code : ", rc)

    def on_disconnect(client, userdata, flags, rc=0):
        print("Disconnected result code : ", str(rc))

    def on_publish(client, userdata, mid):
        print("In on_pub callback mid= ", mid)

    def on_log(client, userdata, level, buf):
        print(f"log: {buf}")

    print('connect to broker')
    # 새로운 클라이언트 생성
    client_id = f"mqtt_client_{random.randint(0, 1000)}"
    client = mqtt.Client(client_id)

    # 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속중료), on_publish(메세지 발행)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish
    client.on_log = on_log

    # address : localhost, port: 1883 에 연결
    # self.client.connect('localhost', 1883)
    client.connect(get_property('URLs', 'mqtt_sever'), int(get_property('URLs', 'mqtt_port')), 60)

    return client

def bub_message(topic, message):
    client = connect_mqtt()
    client.loop_start()
    # topic 으로 메세지 발행
    msg = f"messages: '{message}'"
    result = client.publish(topic, msg)
    client.loop_stop()
    # 연결 종료
    client.disconnect()


class mos_subscriber:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        print("find created connection....")
        return cls._instance

    def __init__(self):
        cls = type(self)
        if not hasattr(cls, "_init"):
            print("Start create connection....")
            self.client = self.connect_mqtt()
            print("Start create connected....")
            cls._init = True
            self.client.subscribe("#")
            self.client.loop_forever()

    # def sub_message(self):
    #     print('Waiting topic.....')
    #     self.client.subscribe("#")
    #     self.client.loop_forever()

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            print('on_connect called!!!!!!!!')
            # client.subscribe(self.topic)
            if rc == 0:
                print("Connected to MQTT broker OK....")
                self.connected_to_broker = True
            else:
                print("Failed to connect, result code : ", rc)

        def on_disconnect(client, userdata, flags, rc=0):
            print("Disconnected result code : ", str(rc))

        def on_subscribe(client, userdata, mid, granted_qos):
            print("---------------- on_subscribe")
            print("subscribed: " + str(mid) + " " + str(granted_qos))

        def on_message(client, userdata, msg):
            print("---------------- on_messge")
            print(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")
            self.post_messge(msg)

        def on_log(client, userdata, level, buf):
            print(f"log: {buf}")

        print('connect to broker')
        # 새로운 클라이언트 생성
        client_id = f"mqtt_client_{random.randint(0, 1000)}"
        client = mqtt.Client(client_id)

        # 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속중료), on_publish(메세지 발행)
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_subscribe = on_subscribe
        client.on_message = on_message
        client.on_log = on_log

        # address : localhost, port: 1883 에 연결
        # self.client.connect('localhost', 1883)
        print("----connecting-----")
        client.connect(get_property('URLs', 'mqtt_sever'), int(get_property('URLs', 'mqtt_port')), 60)

        return client

        def post_messge(msg):
            image_folder = get_property('DATA', 'base_dir') + get_property('DATA', 'imgpath')
            usr_id, farm_no, command = msg.topic.split('/')
            try:
                if not os.path.exists(get_property('DATA', 'base_dir')):
                    os.makedirs(get_property('DATA', 'base_dir'))

                if not os.path.exists(get_property('DATA', 'base_dir') + get_property('DATA', 'imgpath')):
                    os.makedirs(get_property('DATA', 'base_dir') + get_property('DATA', 'imgpath'))

                if command in "refresh":
                    # refresh topic인 경우
                    image_data = msg.payload
                    image = Image.open(io.BytesIO(image_data))
                    filename = os.path.join(image_folder, f"{usr_id}_{farm_no}_refresh.jpg")

                elif command == "image":
                    # 기타 topic인 경우
                    # 수신한 메시지의 페이로드를 이미지로 변환
                    image_data = msg.payload
                    image = Image.open(io.BytesIO(image_data))

                    # 현재 시간을 파일명에 포함하여 이미지를 파일로 저장
                    current_time = datetime.now().strftime("%Y-%m-%d %H-%M")
                    filename = os.path.join(image_folder, f"{usr_id}_{farm_no}_{current_time}.jpg")

                image.save(filename)
                print("Received and saved image: " + filename)
            except Exception as e:
                print("Error during image processing: " + str(e))

