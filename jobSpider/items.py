# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobspiderItem(scrapy.Item):
    positionName = scrapy.Field()
    positionLabels = scrapy.Field()
    positionAdvantage = scrapy.Field()
    education = scrapy.Field()
    workYear = scrapy.Field()
    jobNature = scrapy.Field()
    salary = scrapy.Field()
    createTime = scrapy.Field()
    industryField = scrapy.Field()
    industryLabels = scrapy.Field()
    companyName = scrapy.Field()
    companySize = scrapy.Field()
    financeStage = scrapy.Field()
    companyLabelList = scrapy.Field()
    city = scrapy.Field()
    businessZones = scrapy.Field()
    district = scrapy.Field()
    firstType = scrapy.Field()
    secondType = scrapy.Field()
    link = scrapy.Field()
    pass
