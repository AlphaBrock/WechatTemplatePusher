# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name   :     util.py
   Description :     通用函数
   Company     :     AlphaBrock
   Author      :     jcciam@outlook.com
   Date        :     2022/8/22 22:55
-------------------------------------------------
"""
import configparser
import os
import random
from resource.zhDate import ZhDate
from datetime import datetime, date
from time import time, localtime


class ConfigReader(object):

    def __init__(self):
        self.path = "config.ini"
        self.conf = configparser.ConfigParser()
        try:
            if os.path.exists(self.path):
                self.conf.read(self.path, encoding="utf-8")
        except IOError as e:
            raise e


class Utils(object):

    def __init__(self):
        pass

    @staticmethod
    def generateColor():
        randomColor = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
        color_list = randomColor(100)
        return random.choice(color_list)

    @staticmethod
    def getBirthday(birthday, year, today):
        birthday_year = birthday.split("-")[0]
        # 判断是否为农历生日
        if birthday_year[0] == "r":
            r_mouth = int(birthday.split("-")[1])
            r_day = int(birthday.split("-")[2])
            # 今年生日
            birthday = ZhDate(year, r_mouth, r_day).to_datetime().date()
            year_date = birthday
        else:
            # 获取国历生日的今年对应月和日
            birthday_month = int(birthday.split("-")[1])
            birthday_day = int(birthday.split("-")[2])
            # 今年生日
            year_date = date(year, birthday_month, birthday_day)
        # 计算生日年份，如果还没过，按当年减，如果过了需要+1
        if today > year_date:
            if birthday_year[0] == "r":
                # 获取农历明年生日的月和日
                r_last_birthday = ZhDate((year + 1), r_mouth, r_day).to_datetime().date()
                birth_date = date((year + 1), r_last_birthday.month, r_last_birthday.day)
            else:
                birth_date = date((year + 1), birthday_month, birthday_day)
            birth_day = str(birth_date.__sub__(today)).split(" ")[0]
        elif today == year_date:
            birth_day = 0
        else:
            birth_date = year_date
            birth_day = str(birth_date.__sub__(today)).split(" ")[0]
        return birth_day



if __name__ == '__main__':
    aaa = Utils()
    print(aaa.getBirthday("1996-03-30", 2022, "2022-08-23"))
