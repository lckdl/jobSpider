#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/25 19:50
# @Author  : Kevin Liu
# @Site    : 
# @File    : display.py
# @Software: PyCharm

import os
import webbrowser
from pyecharts import Bar, WordCloud, Page
from dataAnalysis.mongoclient import client
import dataAnalysis.cut
from collections import OrderedDict

# get datas
datas = client.find_for_pyecharts({'keyword': 'python'}, ['city'])

# city counter
cities = set(datas['city'])
city_count = {}

for i in cities:
    city_count[i] = datas['city'].count(i)

ordered_count = OrderedDict(sorted(city_count.items(), key=lambda x: x[1], reverse=True))

# detail tags
tags_list = dataAnalysis.cut.da_for_wordcloud()
# filter
names = list(tags_list[0])
values = list(tags_list[1])
filter_strings = ('Python', 'python')
for f in filter_strings:
    values.pop(names.index(f))
    names.remove(f)

bar = Bar("Python")
bar.add("city", list(ordered_count.keys()), list(ordered_count.values()),
        xaxis_interval=0,
        xaxis_rotate=30,
        is_more_utils=True,
        is_label_show=True,
        is_datazoom_show=True)
# bar.render()

wordcloud = WordCloud(width=1000, height=600)
wordcloud.add("", names, values, word_size_range=[20, 100])
# wordcloud.render()

page = Page()
page.add(bar)
page.add(wordcloud)
page.render()
webbrowser.open('file:///' + os.getcwd() + '/render.html')
