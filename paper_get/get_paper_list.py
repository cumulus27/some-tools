#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Get someone's paper list from web.
"""

import os
import time
import urllib
import urllib.parse
import urllib.request
import requests

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0


class PaperList:

    def __init__(self, url):
        self.url = url
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

        while True:
            self.soup = BeautifulSoup(self.source, "html.parser")
            self.start_analysis()
            self.get_next_page()
            if self.is_end:
                break

        self.driver.quit()

    def get_first_page(self):
        # Create a new instance of the Chrome driver
        driver = webdriver.Chrome("tools/chromedriver")

        # go to the target home page
        driver.get(self.url)

        self.source = driver.page_source
        self.driver = driver

        # Get the page number
        self.page_now = self.driver.find_element_by_class_name("res-page-number-now")
        print(f"Page : {self.page_now.get_attribute('data-num')}")

    def get_next_page(self):
        next_page = self.driver.find_element_by_class_name("c-icon-page-next-hover")
        next_page.click()

        time.sleep(1)

        # Get the page number
        self.page_now = self.driver.find_element_by_class_name("res-page-number-now")
        print(f"Page : {self.page_now.get_attribute('data-num')}")

        next_button = self.driver.find_element_by_class_name("c-icon-page-next-hover")
        style = next_button.get_attribute('style')
        if style:
            self.is_end = True

    def start_analysis(self):
        h3s = self.soup.find_all("h3", "res_t")
        for h3 in h3s:
            a = h3.find("a")
            print(a.string)

    def save_in_file(self):
        pass


if __name__ == "__main__":

    url = "http://xueshu.baidu.com/scholarID/CN-BH740BDJ"
    get = PaperList(url)

    get.get_the_site()

