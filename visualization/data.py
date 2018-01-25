#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/25 19:49
# @Author  : Kevin Liu
# @Site    : 
# @File    : data.py
# @Software: PyCharm

from pymongo import *
from jobSpider.settings import MONGODB_SERVER, MONGODB_COLLECTION, MONGODB_DB, MONGODB_PORT


class _Database(object):
    def __init__(self):
        connection = MongoClient(
            MONGODB_SERVER,
            MONGODB_PORT
        )
        self._db = connection[MONGODB_DB]
        self._collection = self._db[MONGODB_COLLECTION]

    def find_for_pyecharts(self, cond=None, disp=None):
        """
        return {field:[values]} from (disp)
        :param cond (dict): find condition
        :param disp (list): display field
        :return (dict): {dispField:[values]}
        """
        datas = self.find_for_analyse(cond, disp)
        results = {}
        for i in disp:
            l = []
            list(map(lambda x: l.append(x[i]), datas))
            results[i] = l
        return results

    def find_for_analyse(self, cond=None, disp=None):
        """
        return [documents] list from mongodb
        :param cond (dict): find condition
        :param disp (list): display field
        :return (list): [documents]
        """
        if not isinstance(cond, dict):
            raise Exception("cond must be dict!")
        if not isinstance(disp, list):
            raise Exception("disp must be list")
        proj = {}
        for i in disp:
            proj[i] = 1
        proj['_id'] = 0
        return list(self._collection.find(cond, proj))

    @property
    def db(self):
        return self._db

    @property
    def collection(self):
        return self._collection


client = _Database()
