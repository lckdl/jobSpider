# -*- coding: utf-8 -*-
import scrapy
from jobSpider.items import JobspiderItem

START_NUM = 4080000


class EasylagouSpider(scrapy.Spider):
    name = 'easylagou'
    allowed_domains = ['lagou.com']
    start_url = 'https://www.lagou.com/jobs/'  # + num.html
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

    def start_requests(self):
        for i in range(START_NUM, 1, -1):
            yield scrapy.Request(url=self.start_url + str(i) + '.html', headers=self.header, callback=self.parse)

    def parse(self, response):
        item = JobspiderItem()
        # print(response.text)
        position_content_sel = response.xpath("//div[@class='position-content ']")
        item['positionName'] = ''.join(
            position_content_sel.xpath(".//div[@class='job-name']/@title").extract_first()).strip()
        item['positionLabels'] = ''.join(
            position_content_sel.xpath(".//ul[@class='position-label clearfix']/li/text()").extract_first()).strip()
        item['positionAdvantage'] = ''.join(
            response.xpath("//dd[@class='job-advantage']/p/text()").extract_first()).strip()

        job_request = position_content_sel.xpath(".//dd[@class='job_request']/p/span/text()").extract()
        item['salary'] = job_request[0].strip()
        item['city'] = job_request[1].strip().strip('/')
        item['workYear'] = job_request[2].strip().strip('/')
        item['education'] = job_request[3].strip().strip('/')
        item['jobNature'] = job_request[4].strip().strip('/')
        item['createTime'] = ''.join(
            position_content_sel.xpath(".//p[@class='publish_time']/text()").extract_first()).strip()

        c_fs = response.xpath("//ul[@class='c_feature']/li/text()").extract()
        company_feature = [x for x in [x.strip() for x in c_fs] if x != '']
        item['companyName'] = ''.join(response.xpath("//img[@class='b2']/@alt").extract_first()).strip()
        item['industryField'] = company_feature[0].strip()
        item['financeStage'] = company_feature[1].strip()
        item['companySize'] = company_feature[2].strip()
        # item['industryLabels'] =
        # item['companyLabelList'] =
        # item['businessZones'] =
        # item['district'] =
        # item['firstType'] =
        # item['secondType'] =
        item['detail'] = ''.join(response.xpath("//dd[@class='job_bt']/div").xpath('string(.)').extract_first()).strip()
        item['link'] = response.url
        yield item
