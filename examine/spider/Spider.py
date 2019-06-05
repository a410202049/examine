#!/usr/bin/python
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

import random
from requests import ConnectionError
import requests
import chardet
from config import Config


class Spider(object):

    def get_random_header(self):
        '''
        USER_AGENTS 随机头信息
        '''
        USER_AGENTS = [
            "Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
            "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
            "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 8.1; PAR-AL00 Build/HUAWEIPAR-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044304 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/WIFI Language/zh_CN Process/tools",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A366 MicroMessenger/6.7.3(0x16070321) NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16A366 MicroMessenger/6.7.3(0x16070321) NetType/WIFI Language/zh_HK",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 MQQBrowser/8.8.2 Mobile/15B87 Safari/604.1 MttCustomUA/2 QBWebViewType/1 WKType/1",
            "Mozilla/5.0 (iPhone 6s; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0 MQQBrowser/8.3.0 Mobile/15B87 Safari/604.1 MttCustomUA/2 QBWebViewType/1 WKType/1",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 10_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0 MQQBrowser/8.8.2 Mobile/14B72c Safari/602.1 MttCustomUA/2 QBWebViewType/1 WKType/1",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0_2 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Mobile/15A421 wxwork/2.5.8 MicroMessenger/6.3.22 Language/zh",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 11_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15G77 wxwork/2.5.1 MicroMessenger/6.3.22 Language/zh",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0 MQQBrowser/8.8.2 Mobile/14B100 Safari/602.1 MttCustomUA/2 QBWebViewType/1 WKType/1",
            "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-CN; vivo Y85 Build/OPM1.171019.011) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.9.6.976 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 8.0.0; zh-cn; Mi Note 2 Build/OPR1.170623.032) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.128 Mobile Safari/537.36 XiaoMi/MiuiBrowser/10.1.1",
            "Mozilla/5.0 (Linux; U; Android 7.0; zh-cn; MI 5s Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.128 Mobile Safari/537.36 XiaoMi/MiuiBrowser/10.2.2",
            "Mozilla/5.0 (Linux; U; Android 8.0.0; zh-CN; MI 5 Build/OPR1.170623.032) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.8.9.969 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 5.1.1; zh-CN; SM-J3109 Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/11.8.0.960 UWS/2.12.1.18 Mobile Safari/537.36 AliApp(TB/7.5.4) UCBS/2.11.1.1 WindVane/8.3.0 720X1280",
            "Mozilla/5.0 (Linux; Android 8.0.0; SM-G9650 Build/R16NW; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.83 Mobile Safari/537.36 T7/10.13 baiduboxapp/10.13.0.11 (Baidu; P1 8.0.0)"
        ]

        return {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate',
        }

    def _get_page_html(self, url, header=None, is_proxy=None, proxy_ip=None):
        """
        获取html
        :param url:
        :param header:
        :param is_proxy:
        :param proxy_ip:
        :return:
        """
        if is_proxy:
            proxies = {
                "http": "http://{proxy_ip}".format(proxy_ip=proxy_ip),
                "https": "https://{proxy_ip}".format(proxy_ip=proxy_ip)
            }
            r = requests.get(url=url, headers=header, timeout=Config.TIMEOUT, proxies=proxies)
            r.encoding = chardet.detect(r.content)['encoding']
            if (not r.ok) or len(r.content) < 500:
                raise ConnectionError
            else:
                return r.text
        else:
            r = requests.get(url=url, headers=header, timeout=Config.TIMEOUT)
            r.encoding = chardet.detect(r.content)['encoding']
            if (not r.ok) or len(r.content) < 500:
                raise ConnectionError
            else:
                return r.text

    def page_download(self, url, header=None, is_proxy=False, proxy_ip=None):
        """
        下载页面
        :param url:
        :param is_proxy是否开启代理
        :return:
        """
        try:
            return self._get_page_html(url, header, is_proxy, proxy_ip)

        except Exception as e:
            print(e)
            return None
            # count = 0  # 重试次数
            # while count < Config.RETRY_TIME:
            #     try:
            #         return self._get_page_html(url, header, is_proxy, proxy_ip)
            #     except Exception:
            #         count += 1
