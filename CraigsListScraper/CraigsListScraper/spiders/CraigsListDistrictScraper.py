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
"""
Parses the data, retrieves the name of the district and places in ending_url
Using CraigsListDistrictItem, takes the url value and puts it as name of region
Concatenates the current starting string with the URL as that is the structure of the URL
@return the array of data to be uploaded to a CSV
#TODO: Add a field to the item field that will label to what region the district belongs to
"""
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
