# -*- coding: utf-8 -*-
import scrapy
from jobSpider.items import JobspiderItem
import urllib.parse
import json


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['lagou.com']
    start_ajax = 'https://www.lagou.com/jobs/positionAjax.json?'
    header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'Referer': "https://www.lagou.com/jobs/list_",
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': None,
        'X-Requested-With': "XMLHttpRequest",
    }

    def __init__(self, key=None, **kwargs):
        super().__init__(**kwargs)
        self.search_key = key
        self.search_range = 30
        self.queryString_dict = {
            'needAddtionalResult': False,
            'isSchoolJob': 0,
        }
        self.queryString = urllib.parse.urlencode(self.queryString_dict)

    def start_requests(self):
        if self.search_key is not None:
            for i in range(1, self.search_range + 1):
                url = self.start_ajax + self.queryString
                # formdata values must be string
                formdata = {
                    'first': 'true',
                    'pn': str(i),
                    'kd': self.search_key
                }
                yield scrapy.FormRequest(url=url, method='POST', formdata=formdata, headers=self.header,
                                         callback=self.parse)

    def parse(self, response):
        data = json.loads(response.text, encoding='utf-8')
        if not data['success']:
            self.logger.info(str(data))
            return
        results = data['content']['positionResult']['result']
        for i in results:
            item = JobspiderItem()
            item['positionName'] = i['positionName']
            item['positionLabels'] = i['positionLabels']
            item['positionAdvantage'] = i['positionAdvantage']
            item['education'] = i['education']
            item['workYear'] = i['workYear']
            item['jobNature'] = i['jobNature']
            item['salary'] = i['salary']
            item['createTime'] = i['createTime']
            item['industryField'] = i['industryField']
            item['industryLabels'] = i['industryLabels']
            item['companyName'] = i['companyName']
            item['companySize'] = i['companySize']
            item['financeStage'] = i['financeStage']
            item['companyLabelList'] = i['companyLabelList']
            item['city'] = i['city']
            item['businessZones'] = i['businessZones']
            item['district'] = i['district']
            item['firstType'] = i['firstType']
            item['secondType'] = i['secondType']
            # item['link'] = i['link']
            yield item
