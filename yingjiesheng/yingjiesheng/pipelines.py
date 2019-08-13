# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class YingjieshengPipeline(object):
    def process_item(self, item, spider):
        job_description = ''.join(item['job_description'])
        if job_description:
            item['job_description'] = job_description.replace('\t', '').replace('\n', ' ').replace('\r', '')
        
        return item
