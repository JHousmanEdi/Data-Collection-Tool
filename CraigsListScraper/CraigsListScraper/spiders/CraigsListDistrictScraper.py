import scrapy
from .. import items
import csv
with open('/home/jhous/Documents/DataCollection/CraigsListScraper/CraigsListScraper/items.csv', 'rbU') as csv_file:
    data = csv.reader(csv_file)
    scrapurls = []
    for row in data:
        scrapurls.append(row)
starting = [x[0] for x in scrapurls]
starting.pop(0)

class CraigsListDistrictSpider(scrapy.Spider):
    name = "districtURLSpider"
    start_urls = starting

    def parse(self, response):
        region_head = response.xpath('//*[@id="topban"]/div[1]/h2//text()').extract()
        ending_url = response.xpath('//*[@id="topban"]/div[1]/ul//li//text()').extract()
        incrementer = 0
        data = []
        for url in ending_url:
            item = items.CraigsListDistrict()
            item["district"] = url
            item["url"] = ("{}{}".format(response.url, url))
            data.append(item)
        return data
