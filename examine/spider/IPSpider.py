#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import json
import random

from DB import Db
from model.Proxy import Proxy, SubmitCount
from spider.Spider import Spider
from log import FinalLogger



db = Db()
db.init_db()


class IPSpider(Spider):

    def __init__(self):
        self.db = db
        # 初始化日志类
        logger = FinalLogger().get_logger()
        self.logger = logger

    def _check_proxy_ip(self, proxy_ip):
        """
        检查代理IP是否可用
        :param proxy_ip:
        :return:
        """
        try:
            resp = self.page_download('http://www.baidu.com', is_proxy=True, proxy_ip=proxy_ip)
            if resp:
                return True
        except Exception:
            return False
        return False

    def get_random_ip(self):
        ips = db.session.query(Proxy).all()
        IP_LIST = []
        for ip in ips:
            IP_LIST.append("{ip}:{port}".format(ip=ip.ip, port=ip.port))
        return random.choice(IP_LIST) if IP_LIST else None


    def add_submit_count(self):
        sub = db.session.query(SubmitCount).first()
        sub.count = sub.count + 1
        self.logger.info("成功提交了{num}".format(num=sub.count))
        db.session.merge(sub)
        db.session.commit()

    def get_fee_ip_list(self):
        """
        获取收费IP列表
        :return: 
        """
        import requests

        r = requests.get('http://api.wandoudl.com/api/ip?app_key=34e0770096923994e61de0fd6baabc07&pack=205214&num=1&xy=1&type=2&lb=\r\n&mr=1&')
        ret = json.loads(r.text)
        if ret['code'] == 200:
            ip_list = ret['data']
            return ip_list
        return []


