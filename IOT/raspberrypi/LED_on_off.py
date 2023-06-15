import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

# MQTT 브로커 정보
broker_address = "192.168.1.159"  # MQTT 브로커의 IP 주소
broker_port = 1883  # MQTT 브로커의 포트 번호

# GPIO 핀 모드 설정
GPIO.setmode(GPIO.BOARD)
LED_PIN = 11  # 사용할 GPIO 핀 번호
GPIO.setup(LED_PIN, GPIO.OUT)
# MQTT 클라이언트 생성 및 연결
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    print("MQTT 브로커에 연결되었습니다.")
    client.subscribe("led/control")  # 구독할 토픽 지정

def on_message(client, userdata, msg):
    message = str(msg.payload.decode("utf-8"))
    print("수신된 메시지:", message)

    if message == "on":
            turn_on_led()
    elif message == "off":
            turn_off_led()


def turn_on_led():
    GPIO.output(LED_PIN, GPIO.HIGH)
    print("LED 켜짐")

def turn_off_led():
    GPIO.output(LED_PIN, GPIO.LOW)
    print("LED 꺼짐")

# MQTT 메시지 수신 및 처리를 위한 콜백 함수 등록
client.on_connect = on_connect
client.on_message = on_message

# MQTT 브로커에 연결
client.connect(broker_address, broker_port)

# MQTT 클라이언트를 계속해서 유지하며 메시지를 처리
client.loop_forever()


