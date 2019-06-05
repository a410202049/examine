#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import json
import random
import time

from datetime import datetime

from DB import Db
from config import Config
from model.Proxy import Proxy, SubmitCount
from spider.Spider import Spider
from utils.IPAddress import IPAddresss
from lxml import etree
from utils.compatibility import text_
from Queue import Queue
db = Db()
db.init_db()


class IPSpider(Spider):

    def __init__(self):
        self.ips = IPAddresss(Config.QQWRY_PATH)
        self.proxies = set()
        self.proxies_quequ = Queue()
        self.checked_proxies = Queue()
        self.db = db

    def gather_ips(self, url, parser):
        """
        采集IP
        :return:
        """
        ip_spider = IPSpider()
        if parser.get('header'):
            header = parser['header']
        else:
            header = self.get_random_header()
        response = ip_spider.page_download(url, header=header)
        if response:
            proxylist = ip_spider.parse(response, parser)
            if proxylist is not None:
                for proxy in proxylist:
                    proxy_str = '%s:%s' % (proxy['ip'], proxy['port'])
                    print("采集IP："+proxy_str)
                    if proxy_str not in self.proxies:
                        self.proxies.add(proxy_str)
                        while True:
                            if self.proxies_quequ.full():
                                time.sleep(0.1)
                            else:
                                self.proxies_quequ.put(proxy)
                                break

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

    def check_proxy_ip_list(self):
        """
        检查代理IP列表
        :param proxy_ip:
        :return:
        """
        while True:
            if not self.proxies_quequ.empty():
                proxy = self.proxies_quequ.get(timeout=300)
                if self._check_proxy_ip(proxy['ip']):
                    self.checked_proxies.put(proxy)
                    print("{ip}:{port}验证通过 SUCCESS".format(ip=proxy['ip'], port=proxy['port']))
                else:
                    print("{ip}:{port}未验证通过 ERROR".format(ip=proxy['ip'], port=proxy['port']))
            else:
                break

    def save_checked_proxy(self):
        """
        保存检查过的代理IP
        :param proxy_ip:
        :return:
        """
        while True:
            if not self.checked_proxies.empty():
                proxy = self.checked_proxies.get(timeout=300)

                try:
                    proxy_model = Proxy()
                    proxy_model.area = proxy['area']
                    proxy_model.country = proxy['country']
                    proxy_model.ip = proxy['ip']
                    proxy_model.speed = proxy['speed']
                    proxy_model.port = proxy['port']
                    proxy_model.type = proxy['type']
                    proxy_model.protocol = proxy['protocol']
                    self.db.session.add(proxy_model)
                    self.db.session.commit()
                except Exception as e:
                    print('{ip}:{port}已经存在'.format(ip=proxy['ip'], port=proxy['port']))
                    continue
            else:
                break

    def parse(self, response, parser):
        '''
        :param response: 响应
        :param type: 解析方式
        :return:
        '''
        return self.XpathPraser(response, parser)

    def XpathPraser(self, response, parser):
        '''
        针对xpath方式进行解析
        :param response:
        :param parser:
        :return:
        '''
        proxylist = []
        root = etree.HTML(response)
        proxys = root.xpath(parser['pattern'])
        for proxy in proxys:
            try:
                ip = proxy.xpath(parser['position']['ip'])[0].text
                port = int(proxy.xpath(parser['position']['port'])[0].text)
                type = proxy.xpath(parser['position']['type'])[0].text
                type = 0 if text_('高') in type else 1

                # 设置默认http
                protocol = 'http'
                if parser['position']['protocol']:
                    protocol = (proxy.xpath(parser['position']['protocol'])[0].text).lower()

                protocol = 0 if protocol == 'http' else 1
                addr = self.ips.getIpAddr(self.ips.str2ip(ip))

                if text_('省') in addr or self.AuthCountry(addr):
                    country = text_('国内')
                    area = addr
                else:
                    country = text_('国外')
                    area = addr

                if parser.get('only_china') and country == text_('国外'):
                    continue

            except Exception as e:
                continue

            proxy = {'ip': ip, 'port': port, 'type': type, 'protocol': protocol, 'country': country,
                     'area': area, 'speed': 100}
            proxylist.append(proxy)
        return proxylist

    def AuthCountry(self, addr):
        '''
        用来判断地址是哪个国家的
        :param addr:
        :return:
        '''
        areas = ['河北', '山东', '辽宁', '黑龙江', '吉林', '甘肃', '青海', '河南', '江苏', '湖北', '湖南', '江西', '浙江', '广东', '云南', '福建', '台湾',
                 '海南', '山西', '四川', '陕西', '贵州', '安徽', '重庆', '北京', '上海', '天津', '广西', '内蒙', '西藏', '新疆', '宁夏', '香港', '澳门']

        for area in areas:
            if text_(area) in addr:
                return True
        return False

    def get_random_ip(self):
        ips = db.session.query(Proxy).all()
        IP_LIST = []
        for ip in ips:
            IP_LIST.append("{ip}:{port}".format(ip=ip.ip, port=ip.port))
        return random.choice(IP_LIST) if IP_LIST else None

    def get_db_ip_list(self):
        ips = db.session.query(Proxy).all()
        IP_LIST = []
        for ip in ips:
            IP_LIST.append("{ip}:{port}".format(ip=ip.ip, port=ip.port))
        return IP_LIST

    def add_submit_count(self):
        sub = db.session.query(SubmitCount).first()
        sub.count = sub.count + 1
        print("成功提交了{num}".format(num=sub.count))
        db.session.merge(sub)
        db.session.commit()


    def get_fee_ip_list(self):
        """
        获取收费IP列表
        :return: 
        """
        import requests

        r = requests.get('http://api.wandoudl.com/api/ip?app_key=34e0770096923994e61de0fd6baabc07&pack=205158&num=10&xy=1&type=2&lb=\r\n&mr=2&')
        ret = json.loads(r.text)
        if ret['code'] == 200:
            ip_list = ret['data']
            return ip_list
        return []

    # def str2datetime(input_str):
    #     return datetime.strptime(input_str, '%Y%m%d%H%M%S')

    def save_fee_ip(self, proxy):
        proxy_model = Proxy()
        proxy_model.area = proxy['city']
        proxy_model.country = '中国'
        proxy_model.ip = proxy['ip']
        proxy_model.speed = '100'
        proxy_model.port = proxy['port']
        proxy_model.type = 0
        proxy_model.protocol = 0
        proxy_model.expire_time = datetime.strptime(proxy['expire_time'], '%Y-%m-%d %H:%M:%S')
        self.db.session.add(proxy_model)
        self.db.session.commit()

    def delete_ip(self):
        db.session.query(Proxy).delete()
        db.session.commit()
