import time, os
import datetime
from common.models import Farm, FarmPlant, Disease, SensorData
from config.settings import BASE_DIR

# 날짜, 시간 관련 문자열 형식
FORMAT_DATE = "%Y%m%d"
FORMAT_DATETIME = "%Y%m%d%H%M%S"
propFile = './config.ini'

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
    today_str = today.strftime(FORMAT_DATE)
    return today_str

def get_time_str():
    return datetime.datetime.fromtimestamp(
        int(time.time())).strftime(FORMAT_DATETIME)

def get_refresh_imgpath(username, farm):
    data_dir = get_property('DATA', 'base_dir')
    sub_dir = get_property('DATA', 'imgpath')
    img_path = data_dir+sub_dir+username+'/'+farm+'/refresh.jpg'
    img_path = os.path.join(BASE_DIR,img_path)
    return img_path



