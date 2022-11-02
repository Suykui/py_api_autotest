import re
import os
from utils.com_log import logger
import requests
import json
path  = os.path.abspath(os.path.join(os.path.abspath(__file__), "../.."))

class ComSession(object):
    def __init__(self, address, login_url, login_para) -> None:
        self.session = requests.session()
        self.api_root_url = address
        payload = json.dumps(login_para)
        login_url = self.api_root_url + login_url
        logger.info("req:%s, payload:%s" %(login_url,payload))
        self.session.headers["Content-Type"] = "application/json;charset=UTF-8"
        ret = self.session.post(url=login_url, data=payload)
        if ret.status_code != 200:
            logger.error("login server failed")
            raise Exception("登录服务失败")
        logger.info("ret:%s"%ret.text)
        token = None
        for key in ret.json()["data"]:
            if "token" in key:
                token = ret.json()["data"][key]
        self.session.headers['Authorization'] = "Bearer "+token
        
    
    def check_req(self, url, method='get', payload=None):
        url = self.api_root_url + url
        logger.info("req:%s, params:%s" %(url,payload))
        if method == 'get':
            ret = self.session.get(url=url,params=payload)
        elif method == 'post':
            payload = json.dumps(payload)
            ret = self.session.post(url=url,data=payload)
        elif method == "put":
            payload = json.dumps(payload)
            ret = self.session.put(url=url,data=payload)
        elif method == "delete":
            ret = self.session.delete(url=url,data=payload)
        if ret.status_code != 200:
            logger.error("req failed, ret code:%s" %ret.status_code)
            raise Exception("请求服务失败")
        logger.info("ret:%s"%ret.text)
        # if "500" in ret.text:
        #     logger.error("req failed, ret code:%s" %ret.status_code)
        #     raise Exception("请求服务失败")
        if ret.text and ret.json():
            return ret.json()
        else:
            return None

    def download_file(self, url, method='post', payload=None, filename='downloadtest.txt'):
        url = self.api_root_url + url
        logger.info("req:%s, params:%s" %(url,payload))
        if  method == "post":
            payload = json.dumps(payload)
            ret = self.session.post(url=url,data=payload)
        if ret.status_code != 200:
            logger.error("req failed, ret code:%s" %ret.status_code)
            raise Exception("请求服务失败")
        #logger.info("ret:%s"%ret.text)
        if ret.content:
            with open(path+"/download/"+filename, 'wb') as f:
                f.write(ret.content)