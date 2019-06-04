#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from time import sleep

from gevent import monkey

from examine import AxfExamineVote

monkey.patch_all()

from config import Config
from spider.IPSpider import IPSpider
import gevent
import threading

ip_spider = IPSpider()


def start_spider():
    """
    启动爬虫
    :return:
    """

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
    # 检查线程列表
    check_thread_list = []
    for i in range(1, Config.THREAD_NUM):
        t = threading.Thread(target=ip_spider.check_proxy_ip_list)
        check_thread_list.append(t)

    for t in check_thread_list:
        t.start()

    for t in check_thread_list:
        t.join()
    print("检查线程结束")

    # 保存线程列表
    save_thread_list = []

    for i in range(1, Config.THREAD_NUM):
        t = threading.Thread(target=ip_spider.save_checked_proxy)
        save_thread_list.append(t)

    for t in save_thread_list:
        t.start()

    for t in save_thread_list:
        t.join()
    print("保存线程结束")

if __name__ == '__main__':
    while True:
        ip_spider.delete_ip()
        start_spider()
        sleep(60*30)
