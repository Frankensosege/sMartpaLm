import time, os
import datetime
from common.models import Farm, FarmPlant, Disease, SensorData

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


def get_context_palm(request, context=None):
    user = request.user
    username = user.username
    palm_farms = Farm.objects.filter(user_id=user.id)
    farm_list = list(palm_farms)
    palm_context = {}
    for farm in farm_list:
        palm_values = FarmPlant.objects.filter(id=farm.id)
        if palm_values:
            palm_list = list(palm_values)
            palm_context[Farm.name] = palm_list
    if not context:
        context = {
            'username': username,
            'farm_list': farm_list,
            'palm_context': palm_context
        }
    else:
        context['username'] = username
        context['farm_list'] = farm_list
        context['palm_context'] = palm_context

    return context

def get_refresh_imgpath():
    data_dir = get_property('DATA', 'base_dir')
    sub_dir = get_property('DATA', 'imgpath')
    img_path = data_dir+sub_dir+'refresh.jpg'
    return img_path



