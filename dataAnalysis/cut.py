#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/25 23:38
# @Author  : Kevin Liu
# @Site    : 
# @File    : cut.py
# @Software: PyCharm

import jieba.analyse
from dataAnalysis.mongoclient import client


def da_for_wordcloud():
    datas = client.find_for_pyecharts({'keyword': 'python'}, ['detail'])
    detail_string = ''.join(datas['detail'])
    seg_list = jieba.analyse.extract_tags(detail_string, topK=20, withWeight=True, allowPOS=('eng', 'n'))
    return list(zip(*seg_list))
