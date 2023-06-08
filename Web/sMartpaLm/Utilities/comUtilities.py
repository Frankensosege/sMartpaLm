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
                {"name": "분석툴관리",
                 "url": "/stkadmin/anal_tool_man/",
                 "submenu": []
                 },
                {"name": "종목관리",
                 "url": "/stkadmin/item_admin/",
                 "submenu": []
                 },
                {"name": "학습관리",
                 "url": "/stkadmin/item_learn/",
                 "submenu": []
                 },
                {"name": "재무제표",
                 "url": "/stkadmin/item_fss/",
                 "submenu": []
                 }
            ]
        }
    elif auth == 'U':
        menu_list = {'menu_items':
            [
                {"name": "포트폴리오",
                 "url": "",
                 "submenu": [
                     {"name": "포트폴리오구성",
                      "url": "/investar/create_portpolio/"},
                     # {"name": "주가동향",
                     #  "url": "/investar/daily_price/"}
                 ],
                 },

                {"name": "분석툴",
                 "url": "",
                 "submenu": [
                     {"name": "분석툴 선택",
                      "url": "/investar/tool_man/"},
                     # {"name": "분석조회",
                     #  "url": "/investar/daily_price/"}
                 ]
                 }
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
