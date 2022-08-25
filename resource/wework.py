# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name   :     wework.py
   Description :     
   Company     :     AlphaBrock
   Author      :     jcciam@outlook.com
   Date        :     2022/8/25 16:53
-------------------------------------------------
"""
import json

import requests
from loguru import logger

from resource.utils import ConfigReader


class Wework(ConfigReader):

    def __init__(self):
        super().__init__()
        self.WECOM_CID = self.conf["Wework"]["WECOM_CID"]
        self.WECOM_SECRET = self.conf["Wework"]["WECOM_SECRET"]
        self.WECOM_AID = self.conf["Wework"]["WECOM_AID"]
        self.WECOM_TOUID = self.conf["Wework"]["WECOM_TOUID"]

    def getAccessToken(self):
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
        params = {
            "corpid": self.WECOM_CID,
            "corpsecret": self.WECOM_SECRET
        }
        try:
            response = requests.get(url, params=params).content
            logger.info(str(response, 'utf-8'))
            access_token = json.loads(response).get('access_token')
            if access_token and len(access_token) > 0:
                return access_token
        except Exception as e:
            logger.error(str(e))
            return False

    def sendMsg(self, text):
        access_token = self.getAccessToken()
        if access_token:
            url = "https://qyapi.weixin.qq.com/cgi-bin/message/send"
            params = {
                "access_token": access_token
            }
            payload = {
                "touser": self.WECOM_TOUID,
                "agentid": self.WECOM_AID,
                "msgtype": "text",
                "text": {
                    "content": text
                },
                "duplicate_check_interval": 1800
            }
            try:
                response = requests.post(url, data=json.dumps(payload), params=params).content
                logger.info(str(response, 'utf-8'))
            except Exception as e:
                logger.error(str(e))

    def sendMsgWithMarkdown(self, text):
        """
        仅支持企业微信查看
        :param text:
        :return:
        """
        access_token = self.getAccessToken()
        if access_token:
            url = "https://qyapi.weixin.qq.com/cgi-bin/message/send"
            params = {
                "access_token": access_token
            }
            payload = {
                "touser": self.WECOM_TOUID,
                "agentid": self.WECOM_AID,
                "msgtype": "markdown",
                "markdown": {
                    "content": text
                },
                "duplicate_check_interval": 1800
            }
            try:
                response = requests.post(url, data=json.dumps(payload), params=params).content
                logger.info(str(response, 'utf-8'))
            except Exception as e:
                logger.error(str(e))