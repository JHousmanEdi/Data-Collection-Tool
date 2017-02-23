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
# class DataStoragePipeline(object):
#     def __init__(self):
#         self.csvwriter = csv.writer(open('data.csv', 'wb'))
#         fields = ['CL_ID','Month','Day','State','Occupation','ToAddress',
#         'WordResume','Company','CompanyDescription','EmailSubject','City',
#         'url','RA']
#         csvwriter.writerow(fields)

class CSVPipeline(object):

  def __init__(self):
    self.files = {}

  @classmethod
  def from_crawler(cls, crawler):
    pipeline = cls()
    crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
    crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
    return pipeline

  def spider_opened(self, spider):
    file = open('%s_items.csv' % spider.name, 'w+b')
    self.files[spider] = file
    self.exporter = CsvItemExporter(file)
    self.exporter.fields_to_export = ['CL_ID','Month','Day','State','Occupation','ToAddress',
    'WordResume','Company','CompanyDescription','EmailSubject','City',
    'url','RA']
    self.exporter.start_exporting()

  def spider_closed(self, spider):
    self.exporter.finish_exporting()
    file = self.files.pop(spider)
    file.close()

  def process_item(self, item, spider):
    self.exporter.export_item(item)
    return item
