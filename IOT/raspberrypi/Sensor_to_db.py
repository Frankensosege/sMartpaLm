#!pip install paho-mqtt mysql-connector-python


import paho.mqtt.client as mqtt
import mysql.connector

# MQTT 브로커 정보
broker_address = "MQTT_BROKER_IP"  # MQTT 브로커의 IP 주소
broker_port = 1883  # MQTT 브로커의 포트 번호
topic = "sensor/data"  # 데이터 수신을 위한 토픽

# MySQL 데이터베이스 정보
db_host = "DB_HOST"  # MySQL 호스트
db_user = "DB_USER"  # MySQL 사용자 이름
db_password = "DB_PASSWORD"  # MySQL 사용자 비밀번호
db_name = "DB_NAME"  # 사용할 데이터베이스 이름

# MQTT 클라이언트 생성 및 연결
client = mqtt.Client()

# MySQL 데이터베이스 연결
db = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

def on_connect(client, userdata, flags, rc):
    print("MQTT 브로커에 연결되었습니다.")
    client.subscribe(topic)  # 구독할 토픽 지정

def on_message(client, userdata, msg):
    message = str(msg.payload.decode("utf-8"))
    print("수신된 메시지:", message)

    # 메시지 파싱 및 데이터 추출
    data = message.split(",")
    if len(data) != 4:
        print("잘못된 형식의 메시지입니다.")
        return

    co2 = float(data[0])
    oxygen = float(data[1])
    temperature = float(data[2])
    humidity = float(data[3])

    # 데이터베이스에 데이터 저장
    cursor = db.cursor()
    query = "INSERT INTO sensor_data (co2, oxygen, temperature, humidity) VALUES (%s, %s, %s, %s)"
    values = (co2, oxygen, temperature, humidity)
    cursor.execute(query, values)
    db.commit()
    cursor.close()

# MQTT 메시지 수신 및 처리를 위한 콜백 함수 등록
client.on_connect = on_connect
client.on_message = on_message

# MQTT 브로커에 연결
client.connect(broker_address, broker_port)

# MQTT 클라이언트를 계속해서 유지하며 메시지를 처리
client.loop_forever()
