# -*- coding: utf-8 -*-
import scrapy
from jobSpider.items import JobspiderItem


class JobSpider(scrapy.Spider):
    name = '51job'
    allowed_domains = ['51job.com']
    start_urls = [
        "http://search.51job.com/jobsearch/search_result.php?fromJs=1&keyword="
    ]

    def __init__(self, key=None, **kwargs):
        super().__init__(**kwargs)
        self.search_key = key

    def start_requests(self):
        if self.search_key is not None:
            url = "http://search.51job.com/jobsearch/search_result.php?fromJs=1&keyword=" + self.search_key
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for sel in response.xpath('//div[@id="resultList"]/div[@class="el"]'):
            item = JobspiderItem()
            item['title'] = ''.join(sel.xpath('p[contains(@class, "t1")]/span/a/text()').extract()).strip()
            item['company_name'] = ''.join(sel.xpath('span[@class="t2"]/a/text()').extract()).strip()
            item['location'] = ''.join(sel.xpath('span[@class="t3"]/text()').extract()).strip()
            item['salary'] = ''.join(sel.xpath('span[@class="t4"]/text()').extract()).strip()
            item['update_time'] = ''.join(sel.xpath('span[@class="t5"]/text()').extract()).strip()
            item['company_desc'] = ''.join(sel.xpath('span[@class="t2"]/a/@href').extract()).strip()
            url = ''.join(sel.xpath('p[contains(@class, "t1")]/span/a/@href').extract()).strip()
            item['link'] = url
            if url:
                yield scrapy.Request(url=url, meta={'item': item}, callback=self.parse_company)
        next_page = response.xpath('//div[@class="dw_page"]//li[@class="bk" and a="下一页"]/a/@href')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_company(self, response):
        item = response.meta['item']
        text = response.xpath('//p[@class="msg ltype"]/text()').extract_first()
        if text:
            try:
                texts = text.split('|')
                if len(texts) == 3:
                    item['company_owner'] = texts[0].strip()
                    item['company_size'] = texts[1].strip()
                    item['company_indus'] = texts[2].strip()
                    yield item
                elif len(texts) == 2:
                    if texts[0].strip()[-2].isnumeric():
                        item['company_size'] = texts[0].strip()
                        item['company_indus'] = texts[1].strip()
                    elif texts[1].strip()[-2].isnumeric():
                        item['company_owner'] = texts[0].strip()
                        item['company_size'] = texts[1].strip()
                    else:
                        item['company_owner'] = texts[0].strip()
                        item['company_indus'] = texts[1].strip()

            except Exception as e:
                self.logger.error(item['link'])
                self.logger.error(e)
                yield item
