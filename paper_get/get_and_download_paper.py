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
    def __init__(self):
        pass

    def send_the_search(self):
        pass

    def download_paper(self):
        pass

    def get_the_link(self):
        pass