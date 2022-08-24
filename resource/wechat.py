# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name   :     wechat.py
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


class Wechat(ConfigReader):

    def __init__(self):
        super().__init__()

    def getAccessToken(self):
        try:
            url = "https://api.weixin.qq.com/cgi-bin/token"
            params = {
                "grant_type": "client_credential",
                "appid": self.conf["Wechat"]["appID"],
                "secret": self.conf["Wechat"]["appSecret"]
            }
            response = requests.request("GET", url, params=params, timeout=30)
            logger.info("获取token返回结果:{}".format(response.text))
            return json.loads(response.text)["access_token"]
        except Exception as e:
            logger.exception(str(e))
            logger.error("由于获取微信Token失败, 因而不在继续执行消息推送!")
            return None

    def senMsg(self, data):
        accessToken = self.getAccessToken()
        if accessToken:
            try:
                url = "https://api.weixin.qq.com/cgi-bin/message/template/send"
                params = {
                    "access_token": accessToken
                }
                for user in self.conf["Wechat"]["toUser"].split(","):
                    payload = {
                                "touser": user,
                                "template_id": self.conf["Wechat"]["templateId"],
                                "url": "http://weixin.qq.com/download",
                                "topcolor": "#FF0000",
                                "data": data
                            }
                    headers = {
                        'Content-Type': 'application/json',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
                    }
                    logger.info("推送内容:{}".format(json.dumps(payload, ensure_ascii=False)))
                    response = requests.request("POST", url, params=params, headers=headers, json=payload, timeout=30)
                    logger.info("返回结果:{}".format(response.text))
            except Exception as e:
                logger.exception("微信推送失败:{}".format(str(e)))