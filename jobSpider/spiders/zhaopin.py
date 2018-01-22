# -*- coding: utf-8 -*-
import scrapy
from jobSpider.items import JobspiderItem


class ZhaopinSpider(scrapy.Spider):
    name = 'zhaopin'
    allowed_domains = ['zhaopin.com']
    start_urls = ['http://zhaopin.com/']

    def __init__(self, key=None, **kwargs):
        super().__init__(**kwargs)
        self.search_key = key

    def start_requests(self):
        urls = [
            'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=全国&kw={0}&p={1}&isadv=0'.format(self.search_key, 0)
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for sel in response.xpath('//table[@class="newlist"]'):
            text = sel.xpath('.//tr[@class="newlist_tr_detail"]').extract()
            if not text:
                continue
            item = JobspiderItem()
            item['title'] = ''.join(sel.xpath('.//td[@class="zwmc"]//text()').extract()).strip()
            item['company_name'] = ''.join(sel.xpath('.//td[@class="gsmc"]//text()').extract()).strip()
            item['location'] = ''.join(sel.xpath('.//td[@class="gzdd"]/text()').extract()).strip()
            item['salary'] = ''.join(sel.xpath('.//td[@class="zwyx"]/text()').extract()).strip()
            item['update_time'] = ''.join(sel.xpath('.//td[@class="gxsj"]/text()').extract()).strip()
            url = sel.xpath('.//td[@class="zwmc"]/div/a/@href').extract_first()
            if url:
                item['link'] = url
                yield scrapy.Request(url=url, meta={'item': item}, callback=self.parse_company)
        next_page = response.xpath('//div[@class="pagesDown"]//li[@class="pagesDown-pos"]/a/@href')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_company(self, response):
        item = response.meta['item']
        yield item
