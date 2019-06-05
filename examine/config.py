#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os


class Config(object):
    QQWRY_PATH = os.path.dirname(__file__) + "/data/qqwry.dat"

    # 默认给抓取的ip分配10分,每次连接失败,减一分,直到分数全部扣完从数据库中删除
    DEFAULT_SCORE = 10

    # 下载页面超时时间
    TIMEOUT = 20

    # 启动线程数量
    THREAD_NUM = 20

    # 重试次数
    RETRY_TIME = 3

    # 从免费代理网站下载时的最大并发
    MAX_DOWNLOAD_CONCURRENT = 5

    # 任务队列
    TASK_QUEUE_SIZE = 4

    # 代理池 采集网站列表
    get_proxy_list = [
        {
            'urls': ['http://www.ip3366.net/free/?stype=%s&page=%s' % (m, n) for m in [1, 2] for n in range(1, 8)],
            'pattern': ".//*[@id='list']/table/tbody/tr[position()>0]",
            'position': {'ip': './td[1]', 'port': './td[2]', 'type': './td[3]', 'protocol': './td[4]'},
            "only_china": True
        },
        {
            'urls': ['https://www.kuaidaili.com/free/inha/%s/' % n for n in range(1, 10)],
            'pattern': ".//*[@id='list']/table/tbody/tr[position()>0]",
            'position': {'ip': './td[1]', 'port': './td[2]', 'type': './td[3]', 'protocol': './td[4]'},
            "only_china": True
        },
        {
            'urls': ['http://www.66ip.cn/%s.html' % n for n in ['index'] + list(range(1, 10))],
            'pattern': ".//*[@id='main']/div/div[1]/table/tr[position()>1]",
            'position': {'ip': './td[1]', 'port': './td[2]', 'type': './td[4]', 'protocol': ''},
            'header': {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Cookie": "__jsluid=f917f45bb9d085c3d32c5a40a2644ef6; __jsl_clearance=1559559625.112|0|YZiTnVJzn9094%2Fh%2ByFUxnSzx8SM%3D; Hm_lvt_1761fabf3c988e7f04bec51acd4073f4=1558403331,1559031710,1559559630; Hm_lpvt_1761fabf3c988e7f04bec51acd4073f4=1559559645",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
            },
            "only_china": True
        },
        # {
        #     'urls': ['http://www.xicidaili.com/%s/%s' % (m, n) for m in ['nn', 'nt', 'wn', 'wt'] for n in range(1, 10)],
        #     'pattern': ".//*[@id='ip_list']/tr[position()>1]",
        #     'position': {'ip': './td[2]', 'port': './td[3]', 'type': './td[5]', 'protocol': './td[6]'},
        #     "only_china": True
        # },
        {
            'urls': ['http://www.kuaidaili.com/proxylist/%s/' % n for n in range(1, 10)],
            'pattern': ".//*[@id='freelist']/table/tbody/tr[position()>0]",
            'position': {'ip': './td[1]', 'port': './td[2]', 'type': './td[3]', 'protocol': './td[4]'},
            "only_china": True
        }
    ]

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.dirname(__file__) + '/data/proxy.db'


class LocalConfig(Config):
    pass


config = {
    'local': LocalConfig
}