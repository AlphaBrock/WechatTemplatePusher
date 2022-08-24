# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name   :     main.py
   Description :     主函数入口
   Company     :     AlphaBrock
   Author      :     jcciam@outlook.com
   Date        :     2022/8/22 23:14
-------------------------------------------------
"""
import json
from datetime import datetime, date
from time import localtime

from apscheduler.executors.pool import ThreadPoolExecutor as ApsThreadPoolExecutor
from apscheduler.schedulers.blocking import BlockingScheduler
from loguru import logger

from resource.apis import API
from resource.utils import Utils, ConfigReader
from resource.wechat import Wechat

wechat = Wechat()
api = API()
common = Utils()
config = ConfigReader()
executors = {
    "default": ApsThreadPoolExecutor(max_workers=3)
}
scheduler = BlockingScheduler(executors=executors, timezone='Asia/Shanghai')


def run():
    weather, temperature = api.weather(config.conf["CityInfo"]["cityCode"])
    inspirationalSayings = api.inspirationalSayings()
    rainbowFart = api.rainbowFart()
    horoscope = api.horoscope()
    healthTips = api.healthTips()
    note_en, note_cn = api.iciba()

    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]

    year = localtime().tm_year
    month = localtime().tm_mon
    day = localtime().tm_mday
    today = datetime.date(datetime(year=year, month=month, day=day))
    week = week_list[today.isoweekday() % 7]

    love_year = int(config.conf["PersonData"]["inLoveDay"].split("-")[0])
    love_month = int(config.conf["PersonData"]["inLoveDay"].split("-")[1])
    love_day = int(config.conf["PersonData"]["inLoveDay"].split("-")[2])
    love_date = date(love_year, love_month, love_day)
    love_days = str(today.__sub__(love_date)).split(" ")[0]

    marry_year = int(config.conf["PersonData"]["marryDay"].split("-")[0])
    marry_month = int(config.conf["PersonData"]["marryDay"].split("-")[1])
    marry_day = int(config.conf["PersonData"]["marryDay"].split("-")[2])
    marry_date = date(marry_year, marry_month, marry_day)
    marry_days = str(today.__sub__(marry_date)).split(" ")[0]

    boyBirthday = common.getBirthday(config.conf["PersonData"]["boyBirthday"], year, today)
    girlBirthday = common.getBirthday(config.conf["PersonData"]["girlBirthday"], year, today)

    data = {
        "date": {
            "value": "{} {}".format(today, week),
            "color": common.generateColor()
        },
        "city": {
            "value": config.conf["CityInfo"]["cityName"],
            "color": common.generateColor()
        },
        "weather": {
            "value": weather,
            "color": common.generateColor()
        },
        "temperature": {
            "value": temperature,
            "color": common.generateColor()
        },
        "love_day": {
            "value": love_days,
            "color": common.generateColor()
        },
        "marry_day": {
            "value": marry_days,
            "color": common.generateColor()
        },
        "note_en": {
            "value": note_en,
            "color": common.generateColor()
        },
        "note_ch": {
            "value": note_cn,
            "color": common.generateColor()
        },

        "pipi": {
            "value": rainbowFart,
            "color": common.generateColor()
        },

        "lucky": {
            "value": horoscope,
            "color": common.generateColor()
        },
        "lizhi": {
            "value": inspirationalSayings,
            "color": common.generateColor()
        },
        "health": {
            "value": healthTips,
            "color": common.generateColor()
        },
        "boyBirthday": {
            "value": boyBirthday,
            "color": common.generateColor()
        },
        "girlBirthday": {
            "value": girlBirthday,
            "color": common.generateColor()
        }
    }
    logger.info(json.dumps(data, ensure_ascii=False))

    scheduler.add_job(func=wechat.senMsg, args=[data], trigger="cron", hour=0, minute=8)
    scheduler.start()


if __name__ == '__main__':
    logger.add("log/WechatTempLatePusher.log", rotation="100 MB", retention='10 days', compression='zip', enqueue=True, level='INFO')
    run()
