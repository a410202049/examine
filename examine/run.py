#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from gevent import monkey

from DB import Db
from model.Proxy import Proxy

monkey.patch_all()


from config import Config
from spider.IPSpider import IPSpider
import gevent


def start_spider():
    """
    启动爬虫
    :return:
    """

    ip_spider = IPSpider()
    spawns = []
    for index, parser in enumerate(Config.get_proxy_list):
        print("正在采集第{index}组网站数据".format(index=index+1))
        for url in parser['urls']:
            ip_spider.gather_ips(url, parser)
            print("正在采集{url}".format(url=url))
            spawns.append(gevent.spawn(ip_spider.gather_ips, url, parser))
            if len(spawns) >= Config.MAX_DOWNLOAD_CONCURRENT:
                gevent.joinall(spawns)
                spawns = []

    ip_spider.check_proxy_ip_list()

    ip_spider.save_checked_proxy()


if __name__ == '__main__':
    start_spider()
