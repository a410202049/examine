#!/usr/bin/python
# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from time import sleep

import re
from selenium import webdriver
from threading import Thread
import random
import pickle
import sys

from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.wait import WebDriverWait

reload(sys)
sys.setdefaultencoding('utf8')

submit_count = 0


class AxfExamineVote(object):
    """
    安心付投票调查
    """

    def __init__(self):
        # self.url = "http://ius.iclick.cn/Survey/Step/3750?userkey=8AC7D7026DA6305CC94B0AEAE36BEC41&page=21"
        self.url = "http://ius.iclick.cn/Survey/Index/3750"
        # http://ius.iclick.cn/Survey/Step/3750?userkey=33CD5237DEA808AAAB2B276B8CAB7A04&page=4
        options = webdriver.ChromeOptions()
        options.add_argument('lang=zh_CN.UTF-8')
        # 设置headers
        options.add_argument('user-agent="' + self.select_user_agent() + '"')
        driver = webdriver.Chrome(chrome_options=options)
        driver.set_page_load_timeout(100)  # 设置超时报错
        driver.set_script_timeout(100)  # 设置脚本超时时间。
        driver.implicitly_wait(100)  # 设置页面加载等待5秒
        # driver.maximize_window()
        driver.delete_all_cookies()
        self.driver = driver
        # 设置等待
        self.wait = WebDriverWait(self.driver, 10, 1)
        self.current_page = 0

    def random_index(self, rate):
        """随机变量的概率函数"""
        #
        # 参数rate为list<int>
        # 返回概率事件的下标索引
        start = 0
        index = 0
        randnum = random.randint(1, sum(rate))

        for index, scope in enumerate(rate):
            start += scope
            if randnum <= start:
                break
        return index

    def is_alert_exist(self):
        try:
            self.driver._switch_to.alert()
            return True
        except NoAlertPresentException as e:
            return False

    def close_alert(self):
        self.driver._switch_to.alert().accept()

    def select_user_agent(self):
        """
        随机获取一个useragent
        :return:
        """
        uas = [
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
            "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Opera/9.80 (Android 2.3.4; Linux; Opera mobi/adr-1107051709; U; zh-cn) Presto/2.8.149 Version/11.10",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0; Baiduspider-ads) Gecko/17.0 Firefox/17.0",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9b4) Gecko/2008030317 Firefox/3.0b4",
            "Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; BIDUBrowser 7.6)",
            "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko",
            "Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50",
            "Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50",
            "Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0",
            "Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11",
            "Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11",
            "Mozilla/5.0 (Macintosh; U; Mac OS X Mach-O; en-US; rv:2.0a) Gecko/20040614 Firefox/3.0.0 ",
            "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.0.3) Gecko/2008092414 Firefox/3.0.3",
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5",
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.14) Gecko/20110218 AlexaToolbar/alxf-2.0 Firefox/3.6.14",
            "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
        ]
        return random.choice(uas)

    def start_vote(self):
        """
        开始投票
        :return:
        """

        self.driver.get(self.url)

        start_btn = self.driver.find_element_by_id('sub')
        start_btn.click()

        while True:
            self.page_action()
            sleep(2)

        # 设置代理
        # options.add_argument('--proxy-server=http://' + ipport)

    def question_year_month_day(self, QBox):
        """
        处理年月日
        :return:
        """
        select_list = QBox.find_elements_by_css_selector('dl dd select')
        year_options = select_list[0].find_elements_by_css_selector('option')  # 年选择
        month_options = select_list[1].find_elements_by_css_selector('option')  # 月选择
        year_element = self.wait.until(lambda diver: year_options[random.randint(1, 14)])
        month_element = self.wait.until(lambda diver: month_options[random.randint(1, 12)])
        if not year_element.get_attribute('checked'):
            year_element.click()
        if not month_element.get_attribute('checked'):
            month_element.click()

    def question_province_city(self, QBox):
        """
        处理省份城市
        :return:
        """
        select_list = QBox.find_elements_by_css_selector('dl dd select')
        province_option = select_list[0].find_elements_by_css_selector('option')  # 省份
        province_element = self.wait.until(lambda diver: province_option[random.randint(1, 34)])
        province_element.click()

        city_option = select_list[1].find_elements_by_css_selector('option')  # 城市
        city_element = self.wait.until(lambda diver: city_option[random.randint(1, len(city_option))])
        city_element.click()

    def question_checkbox(self, QBox, checked_index=None):
        """
        处理多选问题
        :return:
        """
        items = QBox.find_elements_by_css_selector('dl dd')
        items_lenth = len(items)
        if checked_index:
            for index in checked_index:
                element = self.wait.until(lambda diver: items[index].find_element_by_css_selector('input'))
                if not element.get_attribute('checked'):
                    element.click()
        else:
            randint = random.randint(1, items_lenth)
            list_range = range(0, items_lenth)
            random_indexs = random.sample(list_range, randint)
            random_indexs = sorted(random_indexs)
            for index in random_indexs:
                element = self.wait.until(lambda diver: items[index].find_element_by_css_selector('input'))
                if not element.get_attribute('checked'):
                    element.click()

    def question_radio(self, QBox, defalut_index=None):
        """
        处理单选问题
        :return:
        """
        items = QBox.find_elements_by_css_selector('dl dd')
        items_lenth = len(items)
        if defalut_index:
            element = self.wait.until(lambda diver: items[defalut_index].find_element_by_css_selector('input'))
            if not element.get_attribute('checked'):
                element.click()
        else:
            random_index = random.randint(0, items_lenth-1)
            element = self.wait.until(lambda diver: items[random_index].find_element_by_css_selector('input'))
            if not element.get_attribute('checked'):
                element.click()

    def question_matrix_mixed(self, QBox):
        """
        矩阵混合题
        :return:
        """
        tr_list = QBox.find_elements_by_css_selector('tbody tr:not(.thead)')
        tr_list_lenth = len(tr_list)

        # 随机单选框下标
        random_index = random.randint(1, tr_list_lenth)

        randint = random.randint(1, tr_list_lenth)
        list_range = range(0, tr_list_lenth)
        checkbox_random_indexs = random.sample(list_range, randint)
        checkbox_indexs = []
        for checkbox_random in checkbox_random_indexs:
            if checkbox_random != random_index:
                checkbox_indexs.append(checkbox_random)

        td_list = tr_list[random_index].find_elements_by_css_selector('td')
        element = self.wait.until(lambda diver: td_list[1].find_element_by_css_selector('input'))
        if not element.get_attribute('checked'):
            element.click()

        for checkbox_index in checkbox_indexs:
            td_list = tr_list[checkbox_index].find_elements_by_css_selector('td')
            element = self.wait.until(lambda diver: td_list[0].find_element_by_css_selector('input'))
            if not element.get_attribute('checked'):
                element.click()

    def question_matrix_radio(self, QBox):
        """
        矩阵单选题
        :return:
        """
        tr_list = QBox.find_elements_by_css_selector('tbody tr:not(.thead)')

        for tr in tr_list:
            randint = random.randint(0, 2)
            td_list = tr.find_elements_by_css_selector('td')
            element = self.wait.until(lambda diver: td_list[randint].find_element_by_css_selector('input'))
            if not element.get_attribute('checked'):
                element.click()

    def question_matrix_checkbox(self, QBox):
        """
        矩阵多选题
        :return:
        """
        tr_list = QBox.find_elements_by_css_selector('tbody tr:not(.thead)')
        tr_list_lenth = len(tr_list)

        randint = random.randint(1, tr_list_lenth)
        list_range = range(0, tr_list_lenth)
        random_indexs_left = random.sample(list_range, randint)

        randint = random.randint(1, tr_list_lenth)
        list_range = range(0, tr_list_lenth)
        random_indexs_right = random.sample(list_range, randint)

        try:
            on_day_tr_element = QBox.find_element_by_xpath('//th[contains(text(),"一日三餐")]//parent::tr')
            td_list = on_day_tr_element.find_elements_by_css_selector('td')
            element = self.wait.until(lambda diver: td_list[0].find_element_by_css_selector('input'))
            if not element.get_attribute('checked'):
                element.click()
        except Exception as e:
            print(e)

        for random_index in random_indexs_left:
            td_list = tr_list[random_index].find_elements_by_css_selector('td')
            element = self.wait.until(lambda diver: td_list[0].find_element_by_css_selector('input'))
            if not element.get_attribute('checked'):
                sleep(2)
                element.click()

        for random_index in random_indexs_right:
            td_list = tr_list[random_index].find_elements_by_css_selector('td')
            element = self.wait.until(lambda diver: td_list[1].find_element_by_css_selector('input'))
            if not element.get_attribute('checked'):
                sleep(2)
                element.click()

    def question_most_checkbox(self, QBox, num=1):
        """
        最多选
        :return:
        """
        dd_list = QBox.find_elements_by_css_selector('dl dd')
        dd_list_lenth = len(dd_list)

        list_range = range(0, dd_list_lenth)
        random_indexs = random.sample(list_range, num)
        for random_index in random_indexs:
            element = self.wait.until(lambda diver: dd_list[random_index].find_element_by_css_selector('input'))
            if not element.get_attribute('checked'):
                element.click()

    def page_action(self):
        # 获取问题列表

        try:
            pnowtxt = self.driver.find_element_by_id('pnowtxt')
            self.current_page = int(pnowtxt.text)
        except Exception as e:
            print e

        QBoxs = self.driver.find_elements_by_class_name('QBox')

        for QBox in QBoxs:
            q_type = ''
            try:
                tcaption = QBox.find_element_by_class_name('tcaption')
                q_type = tcaption.text.replace("（", "").replace("）", "")
            except Exception as e:
                print(e)
                print('未获取到 tcaption')

            if not q_type:
                q_title = QBox.find_element_by_css_selector('h3 p').text
                if '出生年月' in q_title:
                    self.question_year_month_day(QBox)
                elif '省份和城市' in q_title:
                    self.question_province_city(QBox)
            else:
                if q_type == '多选题':
                    if self.current_page == 1:
                        self.question_checkbox(QBox, [8])
                    else:
                        self.question_checkbox(QBox)
                elif q_type == '单选题':
                    if self.current_page == 2:
                        self.question_radio(QBox, 1)
                    else:
                        self.question_radio(QBox)
                elif q_type == '矩阵混合题':
                    self.question_matrix_mixed(QBox)
                elif q_type == '矩阵单选题':
                    self.question_matrix_radio(QBox)
                elif q_type == '矩阵多选题':
                    self.question_matrix_checkbox(QBox)
                elif '最多选' in q_type:
                    num = int(re.search('(\d+)', q_type).group())
                    self.question_most_checkbox(QBox, num)


        sleep(2)
        self.driver.find_element_by_id('submitbutton').click()
        if self.driver.find_element_by_id('submitbutton').text == u'完成提交':
            print("完成{0}次提交".format(submit_count))
            global submit_count
            submit_count += 1
            self.driver.quit()


if __name__ == '__main__':
    AxfExamineVote().start_vote()
