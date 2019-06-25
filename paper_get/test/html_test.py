#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Test google html.
"""

import re
import difflib
from bs4 import BeautifulSoup

with open("../data/test4.html", "r") as f:
    html = f.read()

# print(html)

source = "基于双边滤波的极化SAR相干斑抑制"
name_en = "S Wang"
name_ch = "王爽"

soup = BeautifulSoup(html, "html.parser")

div0 = soup.find("div", id="gs_res_ccl_mid")

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

    sim = difflib.SequenceMatcher(None, source, title).quick_ratio()
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
        if name_en in author_list:
            result_cid = cid
            break
    elif "，" in author:
        # Chinese
        print("The name is Chinese")
        author_list = [name.strip() for name in author.split("，")]
        if name_ch in author_list:
            result_cid = cid
            break
    else:
        # There is only one author
        print("Only one name")
        author_list = author
        if name_en in author_list:
            result_cid = cid
            break
        elif name_ch in author_list:
            result_cid = cid
            break
else:
    print("Can't find the paper.")
    raise RuntimeError

print(result_cid)

div_cite0 = soup.find("div", id="gs_citt")

th = div_cite0.find(text=re.compile("MLA")).parent
print(th)
td = th.next_sibling
print(td.div.get_text())
