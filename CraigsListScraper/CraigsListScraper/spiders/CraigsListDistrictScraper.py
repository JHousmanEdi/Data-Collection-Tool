import scrapy
from .. import items
import csv
"""
Takes CSV Data from the Region Scraper and puts it into a list that Scrapy can utilize as its start_urls
"""
with open('/home/jhous/Documents/DataCollection/CraigsListScraper/CraigsListScraper/items.csv', 'rbU') as csv_file:
    data = csv.reader(csv_file)
    scrapurls = []
    for row in data:
        scrapurls.append(row)
starting = [x[0] for x in scrapurls]
starting.pop(0)
"""
Craigslist spider that will go through subdistricts within regions of an area (I.E. Central Chicago versus City of Chicago)
"""


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
            url_string = str(response.url)
            region_name = url_string[url_string.find("//")+2:url_string.find(".")]
            item["district"] = url
            item["url"] = ("{}{}".format(response.url, url))
            item["region"] = region_name
            data.append(item)
        return data
