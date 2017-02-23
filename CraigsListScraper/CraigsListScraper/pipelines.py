# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter
import settings


class CraigslistscraperPipeline(object):
    def process_item(self, item, spider):
        return item
class DataStoragePipeline(object):
    def __init__(self):
        self.csvwriter = csv.writer(open('data.csv', 'wb'))

    def process_item(self, item, spider):
            fields = ['CL_ID','Month','Day','State','Occupation','ToAddress',
            'WordResume','Company','CompanyDescription','EmailSubject','City',
            'url', 'RA']
            row = [item['CL_ID'][0]]
            for i in fields:
                row.extend(fields)
            self.csvwriter.writerow(row)
            return item
