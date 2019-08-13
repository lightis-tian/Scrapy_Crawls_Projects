# -*- coding: utf-8 -*-
import scrapy
from yingjiesheng.items import YingjieshengItem
import logging


class YjJobsSpider(scrapy.Spider):
    name = 'yj_jobs'
    allowed_domains = ['http://www.yingjiesheng.com']
    start_urls = ['http://www.yingjiesheng.com/shanghai-morejob-1.html']
    host = 'http://www.yingjiesheng.com'

    for i in range(2, 101):    # 最大页数为435
        url = 'http://www.yingjiesheng.com/shanghai-morejob-{}.html'.format(i)
        start_urls.append(url)

    def parse(self, response):
        logging.info('首页相关错误')
        item = YingjieshengItem()
        job_url_list = response.xpath('//td[@class="item1"]/a/@href').extract()
        for each_url in job_url_list:
            if each_url[0] == '/':
                item['job_url'] = self.host + each_url
                yield scrapy.Request(self.host + each_url, dont_filter=True, callback=self.parse_normal_page, meta={'item': item})
            else:
                item['job_url'] = each_url
                yield scrapy.Request(each_url, meta={'item': item}, dont_filter=True, callback=self.parse_vip_page)

    def parse_normal_page(self, response):
        logging.info('普通页面相关错误')
        item = response.meta['item']
        company = response.xpath('//div[@class="job"]/div[2]/text()')[0].extract()
        company_index = company.find(':')
        company_type = response.xpath('//div[@class="job"]/div[2]/text()')[1].extract()
        company_type_index = company_type.find(':')
        item['company'] = company[company_index + 1:]
        item['company_type'] = company_type[company_type_index + 1:]
        item['date'] = response.xpath('//div[@class="info clearfix"]/ol/li[1]/u/text()').extract()
        item['address'] = response.xpath('//div[@class="info clearfix"]/ol/li[2]/u/text()').extract()
        item['job_name'] = response.xpath('//div[@class="info clearfix"]/ol/li[5]/u/text()').extract()
        job_intro = response.xpath('//div[@class="job"]/div[1]')
        item['job_description'] = job_intro.xpath('string(.)').extract()
        yield item

    def parse_vip_page(self, response):
        logging.info('vip页面相关错误')
        item = response.meta['item']
        item['company'] = response.xpath('//div[@class="section"]/h1/a/text()').extract()
        item['date'] = response.xpath('//div[@class="job_list"]/ul/li[2]/span/text()').extract()
        item['company_type'] = response.xpath('//ul[@class="company_detail clearfix"]/li[3]/span/text()').extract()
        item['industry_type'] = response.xpath('//div[@class="section"]/ul/li[1]/span/text()').extract_first()
        item['address'] = ['上海']
        item['job_description'] = response.xpath('//div[@class="j_i"]/text()').extract()
        yield item