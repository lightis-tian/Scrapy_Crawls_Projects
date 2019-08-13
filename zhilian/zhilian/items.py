# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhilianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date = scrapy.Field()
    job_name = scrapy.Field()
    job_url = scrapy.Field()
    company_id = scrapy.Field()
    city = scrapy.Field()
    company = scrapy.Field()
    company_type = scrapy.Field()
    salary = scrapy.Field()
    address = scrapy.Field()
    experience = scrapy.Field()
    education = scrapy.Field()
    people_num = scrapy.Field()
    job_description = scrapy.Field()
