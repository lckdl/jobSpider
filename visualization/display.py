#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/25 19:50
# @Author  : Kevin Liu
# @Site    : 
# @File    : display.py
# @Software: PyCharm

import os
import webbrowser
from pyecharts import Bar
from visualization.data import client
from collections import OrderedDict

# get datas
datas = client.find_for_pyecharts({'keyword': 'python'}, ['city'])

# city counter
cities = set(datas['city'])
city_count = {}

for i in cities:
    city_count[i] = datas['city'].count(i)

ordered_count = OrderedDict(sorted(city_count.items(), key=lambda x: x[1], reverse=True))
bar = Bar("Python")
bar.add("city", list(ordered_count.keys()), list(ordered_count.values()),
        xaxis_interval=0,
        xaxis_rotate=30,
        is_more_utils=True,
        is_label_show=True,
        is_datazoom_show=True)
bar.render()

webbrowser.open('file:///' + os.getcwd() + '/render.html')
