#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Test google html.
"""

import difflib
from bs4 import BeautifulSoup

with open("../data/test.html", "r") as f:
    html = f.read()

# print(html)

source = "复杂分布数据的二阶段聚类算法"

soup = BeautifulSoup(html, "html.parser")

div0 = soup.find("div", id="gs_res_ccl_mid")

# print(div0)

div1s = div0.find_all("div", "gs_r")

titles = []
sims = []
for div1 in div1s:
    h3 = div1.find("h3", "gs_rt")
    a = h3.find("a")
    title = a.get_text()
    titles.append(title)

    sim = difflib.SequenceMatcher(None, source, title).quick_ratio()
    sims.append(sim)

max_sim = max(sims)

print(sims)
print(max_sim)

index = sims.index(max_sim)
print(titles[index])