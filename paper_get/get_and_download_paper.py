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
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0


class PaperDownload:
    def __init__(self, title_list):
        self.driver = None
        self.soup = None
        self.source = None

        self.title_gen = self.get_one_paper_title(title_list)

    def open_the_site(self):
        driver = webdriver.Chrome("tools/chromedriver")
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

            self.source = self.driver.page_source

    def download_paper(self):
        pass

    def get_the_cite(self):
        pass

    def start_download(self):
        while True:
            try:
                self.send_the_search()
            except StopIteration:
                print("There is no more title, finished.")
                self.driver.quit()
                break
            else:
                self.soup = BeautifulSoup(self.source, "html.parser")
                self.get_the_cite()
                self.download_paper()

    @classmethod
    def get_one_paper_title(cls, path):
        with open(path, "r") as f:
            while True:
                name = f.readline().strip()
                if not name:
                    raise StopIteration
                yield name


if __name__ == "__main__":

    tile_list = "data/list.txt"
    down = PaperDownload(tile_list)

    down.start_download()
