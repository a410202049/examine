#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from config import Config
from spider.IPSpider import IPSpider
from multiprocessing import Queue, Process, Value
import time


def start_spider():
    """
    启动爬虫
    :return:
    """
    ip_spider = IPSpider()
    for parser in Config.get_proxy_list:
        ip_spider.gather_ips(parser)
    quequ_list = ip_spider.proxies_quequ
    print quequ_list


if __name__ == '__main__':
    start_spider()
