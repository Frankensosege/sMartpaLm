import paho.mqtt.client as mqtt
import json
class MosPub:
    def __init__(self):
        # 새로운 클라이언트 생성
        self.client = mqtt.Client()
        # 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속중료), on_publish(메세지 발행)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_publish = self.on_publish
        # address : localhost, port: 1883 에 연결
        self.client.connect('localhost', 1883)

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("connected OK")
        else:
            print("Bad connection Return code : ", rc)

    def on_disconnect(client, userdata, flags, rc=0):
        print(str(rc))

    def on_publish(client, userdata, mid):
        print("In on_pub callback mid= ", mid)

    def bub_message(self, message):
        self.client.loop_start()
        # common topic 으로 메세지 발행
        self.client.publish('common', json.dumps({"success": "ok"}), 1)
        self.client.loop_stop()
        # 연결 종료
        self.client.disconnect()

class MosSub:
    def __init__(self):
        # 새로운 클라이언트 생성
        self.client = mqtt.Client()
        # 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속중료), on_publish(메세지 발행)
        self.client.on_connect = self.on_connect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_publish = self.on_publish
        # address : localhost, port: 1883 에 연결
        self.client.connect('localhost', 1883)

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("connected OK")
        else:
            print("Bad connection Return code : ", rc)

    def on_disconnect(client, userdata, flags, rc=0):
        print(str(rc))

    def on_subscribe(client, userdata, mid, granted_qos):
        print("subscribed: " + str(mid) + " " + str(granted_qos))

    def sub_message(self, message):
        self.client.connect('localhost', 1883)
        # common topic 으로 메세지 발행
        self.client.subscribe('common', 1)
        self.client.loop_forever()


