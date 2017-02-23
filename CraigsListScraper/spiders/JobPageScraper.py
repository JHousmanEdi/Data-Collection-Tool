import csv
import scrapy
from .. import items
import os

region_urls_data_path = os.path.join(os.getcwd(), 'region_urls.csv')
district_urls_data_path = os.path.join(os.getcwd(), 'district_urls.csv')

scrapurls = []
with open(region_urls_data_path, 'rbU') as csv_file:
    data = csv.reader(csv_file)
    for row in data:
        scrapurls.append(row)
with open(district_urls_data_path, 'rbU') as csv_file:
    data = csv.reader(csv_file)
    for row in data:
        scrapurls.append(row)
starting = [x[0] for x in scrapurls]
starting.pop(0)


class CraigsListJobpider(scrapy.Spider):
    name = "jobsURLSpider"
    start_urls = starting

    def parse(self, response):
        job_names = response.xpath('//*[@id="jjj0"]/li/a//text()').extract()
        job_urls = response.xpath('//*[@id="jjj0"]/li/a/@href').extract()
        data = []
        for index, url in enumerate(job_urls):
            item = items.CraigsListJobs()
            url_string = str(response.url)
            region_name = url_string[url_string.find("//") + 2:url_string.find(".")]
            district_name = url_string[url_string.find(".org") + 1:url_string.find("/")]
            item["district"] = district_name
            item["url"] = ("{}{}".format(response.url, url[1:]))
            item["region"] = region_name
            item['job_name'] = job_names[index]
            data.append(item)
        return data
