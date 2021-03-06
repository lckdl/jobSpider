# -*- coding: utf-8 -*-
import scrapy
from jobSpider.items import JobspiderItem
import urllib.parse
import json
import math

leadingCities = [
    '北京', '上海', '深圳', '广州', '杭州', '成都', '南京', '武汉', '西安', '厦门', '长沙', '苏州', '天津', '重庆',
    '郑州', '青岛', '合肥', '福州', '济南', '大连', '珠海', '无锡', '佛山', '东莞', '宁波', '常州', '沈阳',
    '石家庄', '昆明', '南昌', '南宁', '哈尔滨', '海口', '中山', '惠州', '贵阳', '长春', '太原', '嘉兴', '泰安',
    '昆山', '烟台', '兰州', '泉州',
]

itemPerPage = 15
needDetail = False


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['lagou.com']
    start_url = 'https://www.lagou.com/jobs/list_'
    start_ajax = 'https://www.lagou.com/jobs/positionAjax.json?'
    header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': None,
        'X-Requested-With': "XMLHttpRequest",
    }

    def __init__(self, key=None, **kwargs):
        super().__init__(**kwargs)
        self.search_key = key

    def start_requests(self):
        if self.search_key is not None:
            self.start_url = self.start_url + self.search_key
            for city in leadingCities:
                query_string_dict = {'needAddtionalResult': False, 'isSchoolJob': 0, 'city': city}
                query_string = urllib.parse.urlencode(query_string_dict)
                yield scrapy.Request(url=self.start_url + '?' + query_string,
                                     headers=self.header,
                                     meta={'queryString_dict': query_string_dict},
                                     callback=self.parse)

    def parse(self, response):
        parse_json_is_ready = False
        title_count = response.xpath("//a[@id='tab_pos']/span/text()").extract_first()
        if not title_count:
            return
        query_string_dict = response.meta['queryString_dict']
        if not title_count == '500+':
            parse_json_is_ready = True  # count < 500
        else:  # too many results
            if 'district' not in query_string_dict:  # extract districts
                districts = response.xpath("//div[@data-type='district']/a/text()").extract()
                query_string_dict['district'] = districts[1]
                query_string = urllib.parse.urlencode(query_string_dict)
                yield scrapy.Request(url=self.start_url + '?' + query_string,
                                     headers=self.header,
                                     meta={'queryString_dict': query_string_dict, 'districts': districts},
                                     callback=self.parse)
            else:  # already exist city & district
                parse_json_is_ready = True

        if not parse_json_is_ready:
            return
        query_string_for_ajax = urllib.parse.urlencode(query_string_dict)
        #  next page (district or city)
        if 'district' in query_string_dict:
            districts = response.meta['districts']
            if not query_string_dict['district'] == districts[-1]:
                index = districts.index(query_string_dict['district'])
                query_string_dict['district'] = districts[index + 1]
                query_string = urllib.parse.urlencode(query_string_dict)
                yield scrapy.Request(url=self.start_url + '?' + query_string,
                                     headers=self.header,
                                     meta={'queryString_dict': query_string_dict, 'districts': districts},
                                     callback=self.parse)
        header = self.header.copy()
        header['Referer'] = response.url
        page = math.ceil(int(title_count) / itemPerPage) if not title_count == '500+' else 30
        url = self.start_ajax + query_string_for_ajax
        if page == 30:
            print(response.url, "too many items")
        for i in range(1, page + 1):
            # formdata values must be string
            formdata = {
                'first': 'true',
                'pn': str(i),
                'kd': self.search_key
            }
            # print(query_string_dict, 'page:', i)
            yield scrapy.FormRequest(url=url, method='POST', formdata=formdata, headers=header,
                                     callback=self.parse_json)

    def parse_json(self, response):
        data = json.loads(response.text, encoding='utf-8')
        if not data['success']:
            self.logger.info(str(data))
            return
        results = data['content']['positionResult']['result']
        for i in results:
            item = JobspiderItem()
            item['positionName'] = i['positionName']
            item['positionLabels'] = i['positionLables']
            item['positionAdvantage'] = i['positionAdvantage']
            item['education'] = i['education']
            item['workYear'] = i['workYear']
            item['jobNature'] = i['jobNature']
            item['salary'] = i['salary']
            item['createTime'] = i['createTime']
            item['industryField'] = i['industryField']
            item['industryLabels'] = i['industryLables']
            item['companyName'] = i['companyFullName']
            item['companySize'] = i['companySize']
            item['financeStage'] = i['financeStage']
            item['companyLabelList'] = i['companyLabelList']
            item['city'] = i['city']
            item['businessZones'] = i['businessZones']
            item['district'] = i['district']
            item['firstType'] = i['firstType']
            item['secondType'] = i['secondType']
            item['link'] = 'https://www.lagou.com/jobs/' + str(i['positionId']) + '.html'
            item['keyword'] = self.search_key
            if needDetail:
                yield scrapy.Request(url=item['link'], headers=response.request.headers, meta={'item': item},
                                     callback=self.parse_detail)
            else:
                yield item

    def parse_detail(self, response):
        item = response.meta['item']
        sel = response.xpath("//dd[@class='job_bt']/div")
        detail = sel.xpath("string(.)").extract_first().strip()
        item['detail'] = detail
        yield item

    def _next_city(self, city):
        if city == leadingCities[-1]:
            return False
        index = leadingCities.index(city)
        return leadingCities[index + 1]
