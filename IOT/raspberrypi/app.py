import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import time, json ,os ,sys
import spidev
import threading
from datetime import datetime, timedelta
from picamera import PiCamera
import signal

# 파일 저장위치
image_folder = "/home/farmer/sMartpaLm/image/"
# MQTT 브로커 정보
broker_address = "16.170.241.38"  # MQTT 브로커의 IP 주소
broker_port = 1883  # MQTT 브로커의 포트 번호
#topic = "{userid}/{farmid}/refresh"
#topic = "{kang}/{farm2}/refresh"
led_topic = "test/farm1/LED"
pub_image_topic = "test/farm1/image_data"
refresh_topic = "test/farm1/refresh"
# LED_status_topic = "test/farm1/LED_status"
mqtt_topic = "test/farm1/sensored_data"

# MQTT 클라이언트 생성 및 연결
client = mqtt.Client()

# def check_led_status():
#     # GPIO 핀 번호 설정
#     LED_PIN = 11
#     # GPIO 모드 설정
#     GPIO.setmode(GPIO.BOARD)

#     # GPIO 핀을 입력 모드로 설정
#     GPIO.setup(LED_PIN, GPIO.IN)
#     led_status = GPIO.input(LED_PIN)
#     if led_status == 1:
#         client.publish(LED_status_topic, payload=b"true", qos=0)
#         print('true')
#     elif led_status == 0:
#         client.publish(LED_status_topic, payload=b"false", qos=0)
#         print('false')

# MQTT 브로커에 이미지를 전송하는 함수
def publish_image(filename, topic):
    with open(filename, "rb") as file:
        image_data = file.read()
        client.publish(topic, payload=image_data, qos=0)

def on_connect(client, userdata, flags, rc):
    print("MQTT 브로커에 연결되었습니다.")
    client.subscribe(led_topic)  # 구독할 토픽 지정
    client.subscribe(refresh_topic)
    # client.subscribe(LED_status_topic)
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    print("수신된 메시지:", msg.payload)
    if msg.payload == b"on":
        turn_on_led()
    elif msg.payload == b"off":
        turn_off_led()
    elif msg.payload == b"refresh":
        filename = "{}current.jpg".format(image_folder)
        # 카메라 설정
        with PiCamera() as camera:
            camera.capture(filename)
            publish_image(filename, refresh_topic+'pub')
            camera.close()
        #true/false
    # elif msg.payload == b"tf":
    #     # check_led_status() 함수를 호출하고 실행이 완료될 때까지 대기
    #     # threading.Thread(target=check_led_status).start()
    #     check_led_status()

# MQTT 메시지 수신 및 처리를 위한 콜백 함수 등록
client.on_connect = on_connect
client.on_message = on_message

# MQTT 브로커에 연결
client.connect(broker_address, broker_port)
# MQTT 클라이언트를 계속해서 유지하며 메시지를 처리
client.loop_start()

# LED 설정
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
LED_PIN = 11  # 사용할 GPIO 핀 번호
GPIO.setup(LED_PIN, GPIO.OUT)

def turn_on_led():
    GPIO.output(LED_PIN, GPIO.HIGH)
    print("LED 켜짐")

def turn_off_led():
    GPIO.output(LED_PIN, GPIO.LOW)
    print("LED 꺼짐")

# 종료 플래그 변수
exit_flag = False

def signal_handler(signal, frame):
    # 사용자가 Ctrl+C를 누를 경우 시그널 핸들러에서 프로그램을 종료합니다.
    print("프로그램이 종료되었습니다.")
    camera=PiCamera()
    global exit_flag
    exit_flag = True
    GPIO.cleanup()
    camera.close()
    thread_capture_image.join()
    thread_sensor_data.join()
    sys.exit(0)  # 프로그램 종료

# 60초 학습데이터 while 루프
def capture_image():
    # 카메라 설정
    camera = PiCamera()
    while not exit_flag:
        # 카메라 켜기
        
        current_time = datetime.now().strftime("%Y-%m-%d_%H:%M")
        filename = "{}{}.jpg".format(image_folder, current_time)
        camera.capture(filename)

        previous_time = (datetime.now() - timedelta(seconds=60)).strftime("%Y-%m-%d_%H:%M")
        previous_filename = "{}{}.jpg".format(image_folder, previous_time)
        if os.path.exists(previous_filename):
            os.remove(previous_filename)

        publish_image(filename, pub_image_topic)
        camera.close()  # 카메라 리소스 해제
        # 60초 동안 대기합니다.
        time.sleep(60)
        camera = PiCamera()  # 새로운 카메라 인스턴스 생성
# 60초 조도센서 while 루프
def pub_sensor_data():
    while not exit_flag:

        #조도센서 설정
        spi = spidev.SpiDev()
        spi.open(0, 0)
        spi.max_speed_hz = 1000000
        spi.bits_per_word = 8

        dummy = 0xff
        start = 0x87
        sgl = 0x40
        ch0 = 0x00
        ch1 = 0x08

        def measure(ch):
            ad = spi.xfer2([(start + sgl + ch), dummy])
            val = (((ad[0] & 0x03) << 8) + ad[1]) * 3.3 / 1023
            return val
                
        mes_ch0 = measure(ch0)
        mes_ch1 = measure(ch1)
        
        timestamp = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        data = {
            "date": timestamp,
            "ch0": mes_ch0,
            "ch1": mes_ch1
        }
        
        print(f'date: {timestamp}, ch0 = {mes_ch0:.2f} [V], ch1 = {mes_ch1:.2f} [V]')
        
        client.publish(mqtt_topic, json.dumps(data))
        
        # 60초 동안 대기합니다.
        spi.close()        
        time.sleep(60)

# Ctrl+C를 처리하기 위한 시그널 핸들러 등록
signal.signal(signal.SIGINT, signal_handler)

# 두 개의 스레드를 생성하여 while 루프를 동시에 실행합니다.
thread_capture_image = threading.Thread(target=capture_image)
thread_sensor_data = threading.Thread(target=pub_sensor_data)

# 스레드를 시작합니다.
thread_capture_image.start()
thread_sensor_data.start()

# 메인 스레드가 종료될 때까지 대기합니다.
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # 사용자가 Ctrl+C를 누를 경우 시그널 핸들러에서 프로그램을 종료합니다.
    signal_handler(signal.SIGINT, None)
