#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/7/19 14:26
# @Author  : Miyouzi
# @File    : GlobalDNS.py
# @Software: PyCharm

import requests, lxml
from bs4 import BeautifulSoup
import re, time


class GlobalDNS():
    def __init__(self, domain, max_retry=3):
        self.__domain = domain
        self.__ip_list = set([])
        self.__dns_id = set([])
        self.__session = requests.session()
        self.__max_retry = max_retry
        self.__token = ''
        self.__src = None
        self.__init_header()

    def __init_header(self):
        # 伪装为Chrome
        host = 'www.whatsmydns.net'
        ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        ref = 'https://' + host + '/'
        lang = 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.6'
        accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        accept_encoding = 'gzip, deflate, br'
        cache_control = 'max-age=0'
        header = {
            "user-agent": ua,
            "referer": ref,
            "accept-language": lang,
            "accept": accept,
            "accept-encoding": accept_encoding,
            "cache-control": cache_control
        }
        self.__req_header = header

    def __request(self, url):
        error_cnt = 0
        while True:
            try:
                f = self.__session.get(url, headers= self.__req_header, timeout=10)
                break
            except requests.exceptions.RequestException as e:
                # print('请求出现异常')
                if error_cnt >= self.__max_retry:
                    raise e
                time.sleep(3)
                error_cnt += 1
        return BeautifulSoup(f.content, "lxml")

    def __get_src(self):
        bf4 = self.__request('https://www.whatsmydns.net/#A/' + self.__domain)
        self.__src = bf4

    def __get_token(self):
        token = self.__src.find('input',id='_token')
        self.__token = token.get('value')
        # print('token= '+self.__token)

    def __get_dns_id(self):
        a = self.__src.find_all('tr')
        for id in a:
            self.__dns_id.add(id.get('data-id'))
        # print(self.__dns_id)

    def __global_query(self):
        for dns_id in self.__dns_id:
            url = 'https://www.whatsmydns.net/api/check?server='+dns_id\
                  +'&type=A&query='+self.__domain\
                  +'&_token='+self.__token
            # print(url)
            try:
                src = self.__request(url)
                # print('src= ',src)
                ips = str(src.contents[0])
                ip = re.findall(r'\d+\.\d+\.\d+\.\d+', ips)
                self.__ip_list = self.__ip_list | set(ip)
            except IndexError:
                pass
                # 该 DNS 失效
        # print(self.__ip_list)

    def get_ip_list(self):

        if len(self.__ip_list) == 0:
            # 如果尚未解析
            self.renew()
        return self.__ip_list

    def renew(self):
        print('正在对 ' + self.__domain + ' 进行全球解析……')
        self.__get_src()
        self.__get_token()
        self.__get_dns_id()
        self.__global_query()
        print(self.__domain + ' 的全球解析已完成')
