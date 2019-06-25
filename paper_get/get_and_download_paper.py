#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Search paper in google.
"""

import os
import re
import time
import random
import difflib
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
    def __init__(self, title_list, name, cite_p, url_p):
        self.driver = None
        self.soup = None
        self.source = None
        self.real_title = None

        self.name_en = name[0]
        self.name_ch = name[1]
        self.cite_p = cite_p
        self.url_p = url_p
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
            self.real_title = one_title.split("->")[0].strip()
            print(self.real_title)

            input_element = self.driver.find_element_by_name("q")
            input_element.clear()
            input_element.send_keys(self.real_title)
            input_element.submit()

            try:
                WebDriverWait(self.driver, 10).until(EC.title_contains(self.real_title[:10]))
            except TimeoutException:
                print("Timeout when open site")
                print(self.driver.title)
                print(self.real_title)
                raise RuntimeError
            else:
                self.source = self.driver.page_source

    def download_paper(self):
        pass

    def get_the_cite(self):
        div0 = self.soup.find("div", id="gs_res_ccl_mid")
        div1s = div0.find_all("div", "gs_r")

        cid_list = []
        cid_data = {}
        title = None
        for div1 in div1s:
            h3 = div1.find("h3", "gs_rt")
            a = h3.find("a")
            data_cid = div1.get("data-cid")
            cid_list.append(data_cid)
            data = {}
            try:
                title = a.get_text()
            except AttributeError:
                # The title does not have a attribute.
                span = h3.find("span", id=data_cid)
                title = span.get_text()
            finally:
                data.update({"title": title})

            sim = difflib.SequenceMatcher(None, self.real_title, title).quick_ratio()
            data.update({"sim": sim})

            # Get the author and periodical
            div2 = div1.find("div", "gs_a")
            try:
                author, periodical, *args = div2.get_text().split("-")
            except AttributeError:
                raise RuntimeError
            else:
                data.update({"author": author})
                data.update({"periodical": periodical})

            cid_data.update({data_cid: data})

        print(cid_list)
        print(cid_data)

        # Sort the result with sim
        cid_sort = sorted(cid_list, key=lambda cid: cid_data[cid]["sim"], reverse=True)
        print(cid_sort)

        # Find the right result with name
        result_cid = None
        for cid in cid_sort:
            author = cid_data[cid]["author"]
            if "," in author:
                # English
                print("The name is English")
                author_list = [name.strip() for name in author.split(",")]
                if self.name_en in author_list:
                    result_cid = cid
                    break
            elif "，" in author:
                # Chinese
                print("The name is Chinese")
                author_list = [name.strip() for name in author.split("，")]
                if self.name_ch in author_list:
                    result_cid = cid
                    break
            else:
                # There is only one author
                print("Only one name")
                author_list = author
                if self.name_en in author_list:
                    result_cid = cid
                    break
                elif self.name_ch in author_list:
                    result_cid = cid
                    break
        else:
            print("Can't find the paper.")
            raise RuntimeError

        print(result_cid)

        # div_result = self.driver.find_element("data-cid", result_cid)
        # div_result = self.driver.find_element_by_css_selector("[data-cid=result_cid]")
        div_rs = self.driver.find_elements_by_class_name("gs_r")
        for div_r in div_rs:
            check_cid = div_r.get_attribute("data-cid")
            if check_cid == result_cid:
                div_result = div_r
                break
        else:
            print("Can't find result element")
            raise RuntimeError

        cite_click = div_result.find_element_by_class_name("gs_or_cit")
        cite_click.click()

        download_a = self.soup.find("a", id=result_cid)
        download_url = ""
        try:
            download_url = download_a.get('href')
        except TypeError:
            print("This paper does't have url")
            download_url = self.real_title + "  [X]"
        finally:
            self.write_in_file(url_path, download_url + "\n")

        time.sleep(2)

        self.source = self.driver.page_source
        self.soup = BeautifulSoup(self.source, "html.parser")

        div_cite0 = self.soup.find("div", id="gs_citt")

        th = div_cite0.find(text=re.compile("MLA")).parent
        print(th)
        td = th.next_sibling
        cite = td.div.get_text()
        print(cite)
        self.write_in_file(self.cite_p, cite + "\n")

        # Click cancel for next search
        cancel = self.driver.find_element_by_id("gs_cit-x")
        cancel.click()

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
    def write_in_file(cls, path, value):
        try:
            with open(path, "a+") as f:
                f.write(value)
        except IOError:
            print("Write failed.")

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
        time.sleep(random.uniform(0.5, 2.5))


if __name__ == "__main__":
    name_en = "S Wang"
    name_ch = "王爽"
    tile_list = "data/test_list.txt"

    cite_path = "data/result/cite.txt"
    url_path = "data/result/url.txt"

    

    down = PaperDownload(tile_list, [name_en, name_ch], cite_path, url_path)

    down.open_the_site()
    down.start_download()
