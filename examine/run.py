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
    for parser in Config.get_proxy_list:
        for url in parser['urls']:
            ip_spider.gather_ips(url, parser)
            spawns.append(gevent.spawn(ip_spider.gather_ips, url, parser))
            if len(spawns) >= Config.MAX_DOWNLOAD_CONCURRENT:
                gevent.joinall(spawns)
                spawns = []

    ip_spider.check_proxy_ip_list()

    # quequ_list = ip_spider.proxies_quequ

    # for proxy in quequ_list:
    #     if ip_spider.check_proxy_ip(proxy):
    #         ip_spider.checked_proxies.put(proxy)

    # for proxy in ip_spider.checked_proxies:
    #     pass

    # print quequ_list


if __name__ == '__main__':
    start_spider()
