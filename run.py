#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/22 16:11
# @Author  : Kevin Liu
# @Site    : 
# @File    : run.py
# @Software: PyCharm

from scrapy import cmdline

# cmdline.execute("scrapy crawl lagou -a key=java".split())
cmdline.execute("scrapy crawl easylagou".split())
# cmdline.execute("scrapy crawlall".split())