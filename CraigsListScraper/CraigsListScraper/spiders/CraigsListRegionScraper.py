import scrapy
from .. import items

"""
Craigslist Spider that gathered all regions URLS and put them with their string name
"""
class CraigsListRegionSpider(scrapy.Spider):
    name = "craigslistRegion_spider"
    allowed_domains = ["craigslist.org"]
    start_urls = ['https://www.craigslist.org/about/sites']
    #/html/body/article/section/div[3]/div[3]/ul[6]/li[1]/a

    def parse(self, response):
        list_of_regions = ["Chicago", "Honolulu", "Los Angeles", "New York", "Phoenix"]
        Single_Regions = ["Albuquerque", "Anchorage", "Billings", "Houston", "Oklahoma City", "Sioux Falls", "Pheonix"]
        Chicago_Regions = ["City of Chicago","North Chicagoland", "South Chicagoland"]
        Honolulu_Regions = ["Oahu"]
        Los_Angeles_Regions = ["Central LA", "San Fernando Valley", "Westside-South Bay", "Long Beach / 562",
                               "San Gabriel Valley"]
        New_York_Regions = ["Brooklyn", "Manhattan", "Queens", "Bronx"]
        all_regions = [list_of_regions, Single_Regions, Chicago_Regions, Honolulu_Regions, Los_Angeles_Regions,
                       New_York_Regions]
        box1_names = response.xpath('/html/body/article/section/div[3]/div[1]//a/text()').extract()
        box1_urls = response.xpath('/html/body/article/section/div[3]/div[1]//a/@href').extract()
        box2_names = response.xpath('/html/body/article/section/div[3]/div[2]//a/text()').extract()
        box2_urls = response.xpath('/html/body/article/section/div[3]/div[2]//a/@href').extract()
        box3_names = response.xpath('/html/body/article/section/div[3]/div[3]//a/text()').extract()
        box3_urls = response.xpath('/html/body/article/section/div[3]/div[3]//a/@href').extract()
        names = box1_names + box2_names + box3_names
        urls = box1_urls + box2_urls + box3_urls
        data = []
        for index, name in enumerate(names):
            item = items.CraigsListRegion()
            item["name"] = name
            item["url"] = urls[index]
            data.append(item)
        return data










