#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Get someone's paper list from web.
"""

import os
import urllib
import urllib.parse
import urllib.request
import requests
from bs4 import BeautifulSoup


class PaperList:

    def __init__(self, url):
        self.url = url
        self.code = None
        self.response = None
        self.response_code = None
        self.response_dict = None
        self.soup = None

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
        url = self.url

        try:
            print("Send a request to url: {}".format(url))
            print("Now waiting...")
            response = requests.get(url)
            print("Successfully get a response. {}".format(response.status_code))

        except urllib.request.HTTPError as e:
            self.handle_http_errors(e.code)
            return 6
        except urllib.request.URLError as e:
            print('URLError: ' + str(e.reason))
            return 5
        except 'Exception' as e:
            import traceback
            print('generic exception: ' + traceback.format_exc())
            return 3
        else:
            if response.status_code != 200:
                print("Not the right response code : {}".format(response.status_code))
                self.handle_http_errors(response.status_code)
                return 4

            result = response.content
            self.response = result.decode('utf8')
            self.soup = BeautifulSoup(self.response, "html.parser")

            # return_code = self.start_analysis()
            # return return_code

    def start_analysis(self):
        pass

    def save_in_file(self):
        pass


if __name__ == "__main__":

    url = "http://xueshu.baidu.com/scholarID/CN-BH740BDJ"
    get = PaperList(url)

    get.get_the_site()
    print(get.response)
