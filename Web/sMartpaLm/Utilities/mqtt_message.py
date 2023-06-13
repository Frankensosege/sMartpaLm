import random
import paho.mqtt.client as mqtt
from Utilities.comUtilities import get_property

class MosPub:
    def __init__(self, topic):
        self.topic = topic
        self.client = self.connect_mqtt()

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
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
        client.connect(get_property('URLs', 'mqtt_sever'), int(get_property('URLs', 'mqtt_port')))

        return client

    def bub_message(self, message):
        self.client.loop_start()
        # topic 으로 메세지 발행
        msg = f"messages: '{message}'"
        result= self.client.publish(self.topic, msg)
        self.client.loop_stop()
        # 연결 종료
        self.client.disconnect()

class MosSub:
    def __init__(self, topic):
        self.topic = topic
        self.client = self.connect_mqtt()

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT broker OK....")
            else:
                print("Failed to connect, result code : ", rc)

        def on_disconnect(client, userdata, flags, rc=0):
            print("Disconnected result code : ", str(rc))

        def on_subscribe(client, userdata, mid, granted_qos):
            print("subscribed: " + str(mid) + " " + str(granted_qos))


        def on_log(client, userdata, level, buf):
            print(f"log: {buf}")

        # 새로운 클라이언트 생성
        client_id = f"mqtt_client_{random.randint(0, 1000)}"
        client = mqtt.Client(client_id)

        # 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속중료), on_publish(메세지 발행)
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_subscribe = on_subscribe
        client.on_log = on_log

        # address : localhost, port: 1883 에 연결
        # self.client.connect('localhost', 1883)
        client.connect(get_property('URLs', 'mqtt_sever'), int(get_property('URLs', 'mqtt_port')))

        return client

    def sub_message(self):
        def on_message(client, userdata, msg):
            print(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")
        # common topic 으로 메세지 발행
        self.client.subscribe(self.topic)
        self.client.on_message = on_message
        self.client.loop_forever()


