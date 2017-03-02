from __future__ import absolute_import
import scrapy
from items import JobInfoGood
import re
import urlparse
import dateutil.parser
import RAOrganizer
#from .. import toAddress_Grabber



class JobDataScraper(scrapy.Spider):
    name = "jobDataSpider"
    data = []
    def __init__(self,RA,*a, **kw):
        super(JobDataScraper, self).__init__(*a, **kw)
        self.RA = RA
        custom_settings = {''}
        print(RA)
        self.urls = RAOrganizer.RAAssignment(RA)
        self.urls.GetURLS()
        self.start_urls = self.urls.URL_Container

        #self.Grabber = toAddress_Grabber.to_AddressFinder

    def parse(self, response):
        links = response.xpath('//*[@id="sortable-results"]/ul/li/p/a/@href').extract()
        starter_split_url = urlparse.urlsplit(response.url)
        current_url = starter_split_url.scheme + "://" + starter_split_url.netloc
        incrementer = 0
        for link in links:
            if link.count('/') <= 2:
                absolute_url = current_url + link
                incrementer+=1
                yield scrapy.Request(absolute_url, callback=self.parse_classified)
            else:
                break

    def parse_classified(self, response):
        data = []
        match = re.search(r"(\w+)\.html", response.url)
        if match:
            item = JobInfoGood()
            #TODO CALL LOGIC ABOUT DETERMINING IF AD IS GOOD OR NOT
            url = response.url
            # self.Grabber.gotoPage(url)
            # if(self.Grabber.check_exists_by_xpath == True):
            #     self.Grabber.Click_Reply
            #     item['toAddress'] = self.Grabber.Obtain_data
            # else:
            #     item['toAddress'] = "Not Available Yet"

            url_split = urlparse.urlsplit(url)
            city = re.split('\W', url_split.netloc)[0]
            item['City'] = city
            item['CL_ID'] = re.split('\W', url_split.path)[2]
            date = response.xpath('//*[@id="display-date"]/time/@datetime').extract()
            date_split = dateutil.parser.parse(date[0])
            date_values = date_split.date()
            item['Month'] = date_values.month
            item['Day'] = date_values.day
            item['url'] = response.url
            data.append(item)

            item['State'] = self.urls.getState(city)
            item['Occupation'] = ""
            item['ToAddress'] = ""
            item['WordResume'] = ""
            item['Company'] = ""
            item['CompanyDescription'] = ""
            item['EmailSubject'] = ""
            item['RA'] = self.urls.RA
            #Acquiring reply request
            #reply_button = response.xpath('//*[@id="replylink"]/@href').extract()
            #reply_request = url_split.scheme + "://" + url_split.netloc + reply_button[0]
            yield item

    # def parse_toaddress(self, response):
    #     print("We are at the address")
    #     item = response.meta['item']
    #     item['toAddress'] = "".join(response.xpath("//div[@class='anonemail']//text()").extract())
    #     self.data.append(item)
    #     return self.data
