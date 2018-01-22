# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobspiderItem(scrapy.Item):
    title = scrapy.Field()              # 职位
    title_requirement = scrapy.Field()  # 职位学位要求
    salary = scrapy.Field()             # 薪水
    update_time = scrapy.Field()        # 更新时间
    link = scrapy.Field()               # 链接
    company_name = scrapy.Field()       # 公司名称
    company_owner = scrapy.Field()      # 公司所有制
    company_size = scrapy.Field()       # 公司人数规模
    company_indus = scrapy.Field()      # 公司行业
    company_desc = scrapy.Field()       # 公司详细信息
    location = scrapy.Field()           # 工作地点
    pass
