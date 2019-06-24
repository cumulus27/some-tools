#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Search paper in google.
"""

import os
import time
import urllib
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0


class PaperDownload:
    def __init__(self, title_list):
        self.driver = None
        self.soup = None
        self.source = None

        self.title_gen = self.get_one_paper_title(title_list)

    def open_the_site(self):
        options = Options()
        # options.headless = True  # do not open UI
        options.add_argument('--proxy-server=socks5://127.0.0.1:1080')

        driver = webdriver.Chrome("tools/chromedriver", chrome_options=options)
        driver.get("https://scholar.google.com")
        self.driver = driver

    def send_the_search(self):
        try:
            one_title = next(self.title_gen)
        except StopIteration:
            raise StopIteration
        else:
            real_title = one_title.split("->")[0].strip()
            print(real_title)

            input_element = self.driver.find_element_by_name("q")
            input_element.send_keys(real_title)
            input_element.submit()

            try:
                WebDriverWait(self.driver, 10).until(EC.title_contains(real_title))
            except TimeoutException:
                pass
            else:
                self.source = self.driver.page_source

    def download_paper(self):
        pass

    def get_the_cite(self):
        pass

    def start_download(self):
        while True:
            self.wait_random_time()
            try:
                self.send_the_search()
            except StopIteration:
                print("There is no more title, finished.")
                self.driver.quit()
                break
            else:
                self.soup = BeautifulSoup(self.source, "html.parser")

                self.wait_random_time()
                self.get_the_cite()

                self.wait_random_time()
                self.download_paper()

    @classmethod
    def get_one_paper_title(cls, path):
        with open(path, "r") as f:
            while True:
                name = f.readline().strip()
                if not name:
                    raise StopIteration
                yield name

    @classmethod
    def wait_random_time(cls):
        pass


if __name__ == "__main__":

    tile_list = "data/test_list.txt"
    down = PaperDownload(tile_list)

    down.open_the_site()
    down.start_download()
