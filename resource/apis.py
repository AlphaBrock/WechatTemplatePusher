# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name   :     apis.py
   Description :     
   Company     :     AlphaBrock
   Author      :     jcciam@outlook.com
   Date        :     2022/8/22 23:00
-------------------------------------------------
"""
import requests
import json
from loguru import logger
from resource.utils import ConfigReader


class API(ConfigReader):

    def __init__(self):
        super().__init__()

    def weather(self, city):
        """
        天气预报
        :param city:
        :return:
        """
        url = "https://restapi.amap.com/v3/weather/weatherInfo"
        params = {
            "city": city,
            "key": self.conf["APIKey"]["weather"]
        }
        try:
            response = requests.request("GET", url, params=params, timeout=30)
            logger.info("天气数据:{}".format(response.text))
            lives = json.loads(response.text)["lives"]
            if len(lives) == 0:
                logger.warning("你所输入的城市:{}有误".format(city))
            weather = lives[0].get("weather")
            temperature = lives[0].get("temperature")
            return weather, temperature
        except Exception as e:
            logger.exception(str(e))
            return "", ""

    def inspirationalSayings(self):
        """
        励志名言
        :return:
        """
        url = "http://api.tianapi.com/lzmy/index"
        payload = {
            "key": self.conf["APIKey"]["tianApi"]
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        try:
            response = requests.request("GET", url=url, params=payload, headers=headers, timeout=30)
            logger.info("获取励志名言数据:{}".format(response.text))
            return json.loads(response.text)["newslist"][0]["saying"]
        except Exception as e:
            logger.exception(str(e))
            return ""

    def rainbowFart(self):
        """
        彩虹屁
        :return:
        """
        url = "http://api.tianapi.com/caihongpi/index"
        payload = {
            "key": self.conf["APIKey"]["tianApi"]
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        try:
            response = requests.request("GET", url=url, params=payload, headers=headers, timeout=30)
            logger.info("获取彩虹屁数据:{}".format(response.text))
            return json.loads(response.text)["newslist"][0]["content"]
        except Exception as e:
            logger.exception(str(e))
            return ""

    def horoscope(self):
        """
        星座运势
        :return:
        """
        url = "http://api.tianapi.com/star/index"
        payload = {
            "key": self.conf["APIKey"]["tianApi"],
            "astro": self.conf["PersonData"]["astro"]
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        try:
            response = requests.request("POST", url=url, params=payload, headers=headers, timeout=30)
            logger.info("获取星座运势数据:{}".format(response.text))
            text = json.loads(response.text)
            data = "速配星座：" + str(text["newslist"][7]["content"]) + "\n爱情指数：" + str(text["newslist"][1]["content"]) + "   工作指数：" + str(
                text["newslist"][2]["content"]) + "\n今日概述：" + str(text["newslist"][8]["content"])
        except Exception as e:
            logger.exception(str(e))
            return ""

    def healthTips(self):
        """
        健康提示
        :return:
        """
        url = "http://api.tianapi.com/healthtip/index"
        payload = {
            "key": self.conf["APIKey"]["tianApi"]
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        try:
            response = requests.request("GET", url=url, params=payload, headers=headers, timeout=30)
            logger.info("获取健康提示数据:{}".format(response.text))
            return json.loads(response.text)["newslist"][0]["content"]
        except Exception as e:
            logger.exception(str(e))
            return ""

    def iciba(self):
        """
        金山词霸
        :return:
        """
        url = "http://open.iciba.com/dsapi/"
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
        }
        try:
            response = requests.request("GET", url=url, headers=headers, timeout=30)
            logger.info("获取金山词霸数据:{}".format(response.text))
            text = json.loads(response.text)
            note_en = text["content"]
            note_cn = text["note"]
            return note_en, note_cn
        except Exception as e:
            logger.exception(str(e))
            return "", ""