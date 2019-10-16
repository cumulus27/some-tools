#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Get someone's paper list from web.
"""

import os
import time
import platform

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class PaperList:

    def __init__(self, urls, path):
        self.url = urls
        self.path = path
        self.source = None
        self.soup = None

        self.driver = None
        self.page_now = None
        self.is_end = False

    @classmethod
    def handle_http_errors(cls, code):
        if code == 404:
            print("Page not find. code 404")
            return 0
        elif code == 403:
            print('You do not have permissions to make that call.\n'
                  'That should not have happened, please contact us.\n[Error 403].')
            return 0
        elif code == 204:
            print('The quota limit has exceeded, please wait and try again soon.\n'
                  'If this problem continues, please contact us.\n[Error 204].')
            return 0
        elif code == 413:
            print("Request Entity Too Large. code 413")
            return 0
        else:
            print('\n[Error ' + str(code) + ']')
            return 0

    def get_the_site(self):
        self.get_first_page()
        self.soup = BeautifulSoup(self.source, "html.parser")
        self.start_analysis()

        self.driver.quit()

    def get_first_page(self):
        # Create a new instance of the Chrome driver
        options = Options()
        system = platform.system()
        if system == "Windows":
            driver = webdriver.Chrome("tools/Windows/chromedriver.exe", chrome_options=options)
        elif system == "Linux":
            driver = webdriver.Chrome("tools/Linux/chromedriver", chrome_options=options)
        else:
            driver = None

        # go to the target home page
        driver.get(self.url)

        # 获取当前的网页源码
        self.source = driver.page_source
        self.driver = driver

    def start_analysis(self):
        divs = self.soup.find_all("div", "res_con")
        for div in divs:
            h3 = div.find("h3", "res_t")
            print(h3.a.string, end=" -> ")
            str_w = h3.a.string + " -> "

            info = div.find("div", "res_info")
            year = info.find("span", "res_year")
            print(year.string, end=" -> ")
            str_w = str_w + year.string + " -> "

            spans = info.find_all("span")
            names = spans[1].find_all("a")
            for name in names:
                if not name.string:
                    break
                print(name.string, end=", ")
                str_w = str_w + name.string + ", "
            else:
                print("\b\b")
                str_w = str_w
            str_w = str_w + "\n"
            self.save_in_file(str_w)

    def save_in_file(self, str_w):
        try:
            with open(self.path, "a+") as f:
                f.write(str_w)
        except IOError as e:
            print(f"Fail to write: {str_w}\nAs error {e}")


if __name__ == "__main__":

    url = "http://xueshu.baidu.com/scholarID/CN-BH740BDJ"
    result_path = "data2/"

    try:
        if not os.path.exists(result_path):
            os.makedirs(result_path)
    except Exception as e:
        print("Error in create path: {}".format(e))

    get = PaperList(url, result_path + "list.txt")

    get.get_the_site()
