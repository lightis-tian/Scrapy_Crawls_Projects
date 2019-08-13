# -*- coding: utf-8 -*-
import scrapy
from zhilian.items import ZhilianItem
import json


class JobsSpiderSpider(scrapy.Spider):
    name = 'jobs_spider'
    start_urls = ['https://fe-api.zhaopin.com/c/i/sou?pageSize=90&cityId=538&salary=0,0&workExperience=-1&education=4&companyType=-1&employmentType=-1&jobWelfareTag=-1&kt=3&=0&_v=0.34726331&x-zp-page-request-id=288eb86dfb8d4d9692a7f0d6b2feb1eb-1561768556928-40960&x-zp-client-id=ef45bbd9-7323-4413-8367-8781cc2579bc']
    for i in range(90, 991, 90):
        page_start = 'start={}&'.format(i)
        urls = 'https://fe-api.zhaopin.com/c/i/sou?{}pageSize=90&cityId=538&salary=0,0&workExperience=-1&education=4&companyType=-1&employmentType=-1&jobWelfareTag=-1&kt=3&=0&_v=0.34726331&x-zp-page-request-id=288eb86dfb8d4d9692a7f0d6b2feb1eb-1561768556928-40960&x-zp-client-id=ef45bbd9-7323-4413-8367-8781cc2579bc'.format(page_start)
        start_urls.append(urls)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_urls)

    def parse_urls(self, response):
        job_list = json.loads(response.text)['data']['results']
        for j in range(0, len(job_list)):
            items = ZhilianItem()
            items['date'] = job_list[j]['updateDate']
            items['job_name'] = job_list[j]['jobName']
            items['job_url'] = job_list[j]['positionURL']
            items['company_id'] = job_list[j]['company']['number']
            items['city'] = job_list[j]['city']['display']
            items['company'] = job_list[j]['company']['name']
            items['company_type'] = job_list[j]['company']['type']['name']
            items['salary'] = job_list[j]['salary']
            items['experience'] = job_list[j]['workingExp']['name']
            items['education'] = job_list[j]['eduLevel']['name']
            items['address'] = job_list[j]['businessArea']
            job_detail_url = job_list[j]['positionURL']
            yield scrapy.Request(job_detail_url, meta={'items': items}, callback=self.parse_job_detail_url, dont_filter=True)

    def parse_job_detail_url(self, response):
        items = response.meta['items']
        items['people_num'] = response.xpath('//ul[@class="summary-plane__info"]/li[4]/text()').extract()
        job_des = response.xpath('//div[@class="describtion__detail-content"]')
        items['job_description'] = job_des.xpath('string(.)').extract()
        yield items