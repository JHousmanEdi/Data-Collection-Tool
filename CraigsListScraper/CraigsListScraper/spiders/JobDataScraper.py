import scrapy
from .. import items
import re
import urlparse
import dateutil.parser



class JobDataScraper(scrapy.Spider):
    name = "jobDataSpider"
    start_urls = ['https://albuquerque.craigslist.org/search/ret']
    data = []

    def parse(self, response):
        links = response.xpath('//*[@id="sortable-results"]/ul/li/p/a/@href').extract()
        starter_split_url = urlparse.urlsplit(response.url)
        current_url = starter_split_url.scheme + "://" + starter_split_url.netloc
        incrementer = 0
        for link in links:
            if link.count('/') <= 2 and incrementer <= 10:
                absolute_url = current_url + link
                incrementer+=1
                yield scrapy.Request(absolute_url, callback=self.parse_classified)
            if incrementer > 10:
                break

    def parse_classified(self, response):
        data = []
        match = re.search(r"(\w+)\.html", response.url)
        if match:
            item = items.JobInfoGood()
            #TODO CALL LOGIC ABOUT DETERMINING IF AD IS GOOD OR NOT
            url = response.url

            url_split = urlparse.urlsplit(url)
            item['City'] = re.split('\W', url_split.netloc)[0]
            item['CL_ID'] = re.split('\W', url_split.path)[2]
            date = response.xpath('//*[@id="display-date"]/time/@datetime').extract()
            date_split = dateutil.parser.parse(date[0])
            date_values = date_split.date()
            item['Month'] = date_values.month
            item['Day'] = date_values.day
            data.append(item)
            '''TO DO
            State
            Occupation
            ToAddress
            WordResume
            Company
            CompanyDescription
            EmailSubject
            '''
            #Acquiring reply request
            #reply_button = response.xpath('//*[@id="replylink"]/@href').extract()
            #reply_request = url_split.scheme + "://" + url_split.netloc + reply_button[0]
            return data

    # def parse_toaddress(self, response):
    #     print("We are at the address")
    #     item = response.meta['item']
    #     item['toAddress'] = "".join(response.xpath("//div[@class='anonemail']//text()").extract())
    #     self.data.append(item)
    #     return self.data















