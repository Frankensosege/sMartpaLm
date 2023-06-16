import json
import time
import datetime
import numpy as np

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

def get_menu_list(auth):
    menu_list = {}

    if auth=='A':
        menu_list = {'menu_items':
            [
                # {"name": "사용자 관리",
                #  "url": "",
                #  "submenu": []
                #  },
                {"name": "사용자관리",
                 "url": "/admin_palm/",
                 "submenu": []
                 },
                {"name": "모델관리",
                 "url": "/admin_palm/",
                 "submenu": []
                 },
                {"name": "농장관리",
                 "url": "/admin_palm/",
                 "submenu": []
                 }
            ]
        }
    elif auth == 'U':
        menu_list = {'menu_items':
            [
                {"name": "내농장관리",
                 "url": "/user_mob/",
                 "submenu": [
                 #     {"name": "농장제어",
                 #      "url": "/user_mob/"},
                     # {"name": "주가동향",
                     #  "url": "/investar/daily_price/"}
                 ]
                 },
                # #
                # # {"name": "농장제어",
                # #  "url": "",
                # #  "submenu": [
                # #      {"name": "제어",
                # #       "url": "/user_mob/"},
                #      # {"name": "분석조회",
                #      #  "url": "/investar/daily_price/"}
                #  ]
                #  }
            ]
        }
    else:
        menu_list = {}

    return json.dumps(menu_list)

def get_today_str():
    today = datetime.datetime.combine(
        datetime.date.today(), datetime.datetime.min.time())
    today_str = today.strftime('%Y%m%d')
    return today_str


def get_time_str():
    return datetime.datetime.fromtimestamp(
        int(time.time())).strftime(FORMAT_DATETIME)
