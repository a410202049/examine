#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os


class Config:
    QQWRY_PATH = os.path.dirname(__file__) + "/data/qqwry.dat"

    # 默认给抓取的ip分配10分,每次连接失败,减一分,直到分数全部扣完从数据库中删除
    DEFAULT_SCORE = 10

    # 下载页面超时时间
    TIMEOUT = 3

    # 重试次数
    RETRY_TIME = 3

    # 从免费代理网站下载时的最大并发
    MAX_DOWNLOAD_CONCURRENT = 5

    # 任务队列
    TASK_QUEUE_SIZE = 4

    # 代理池 采集网站列表
    get_proxy_list = [
        {
            'urls': ['http://www.xicidaili.com/%s/%s' % (m, n) for m in ['nn', 'nt', 'wn', 'wt'] for n in range(1, 2)],
            'pattern': ".//*[@id='ip_list']/tr[position()>1]",
            'position': {'ip': './td[2]', 'port': './td[3]', 'type': './td[5]', 'protocol': './td[6]'}
        }
    ]

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.dirname(__file__) + '/data/proxy.db'


class LocalConfig(Config):
    pass


config = {
    'local': LocalConfig
}