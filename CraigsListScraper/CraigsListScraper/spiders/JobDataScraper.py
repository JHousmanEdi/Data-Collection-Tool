from __future__ import absolute_import
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from items import JobInfoGood
import re
import urlparse
import dateutil.parser
import datetime
import RAOrganizer
import os
from company_finder import classify_text
#from .. import toAddress_Grabber



class JobDataScraper(CrawlSpider):
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
        dates = response.xpath('//*[@id="sortable-results"]/ul/li/p/time/@datetime').extract()
        starter_split_url = urlparse.urlsplit(response.url)
        current_url = starter_split_url.scheme + "://" + starter_split_url.netloc
        today = datetime.date.today()
        max_date = today - datetime.timedelta(days=7)
        max_date_day = max_date.day
        max_date_month = max_date.month
        incrementer = 0
        for index, link in enumerate(links):
            date = dateutil.parser.parse(dates[index])
            post_day = date.day
            post_month = date.month
            if post_day >= max_date_day and post_month >= max_date_month:
                if 'craigslist' in link: #Some links link to other parts of certain areas
                    absolute_url = 'https' + link #Append html to those urls and go on merry way
                else: #If not
                    absolute_url = current_url + link #Its the current url and the ID#
                yield scrapy.Request(absolute_url, callback=self.parse_classified)
            else:
                pass



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
            postid = response.xpath('/html/body/section/section/section/div[2]/p[1]//text()').extract()
            clid = postid[0].split(": ",1)[1]
            item['City'] = city
            item['CL_ID'] = clid
            date = response.xpath('//*[@id="display-date"]/time/@datetime').extract()
            date_split = dateutil.parser.parse(date[0])
            date_values = date_split.date()
            item['Month'] = date_values.month
            item['Day'] = date_values.day
            item['url'] = response.url
            data.append(item)
            item['State'] = self.urls.getState(city)
            item['ToAddress'] = ""

            text = response.xpath('//*[@id="postingbody"]/text()').extract()
            stringed_text = ""
            for i in text:
                stringed_text += i

            item['Occupation'] = ""
            item['WordResume'] = ""
            item['Company'] = classify_text(stringed_text) #Obtains all possible company name values if present
            item['CompanyDescription'] = ""
            item['EmailSubject'] = ""
            item['RA'] = self.urls.RA
            RA_Folder = self.urls.geturlfolder() #Finds folder labeled with name of RA
            filepath = os.path.join(os.getcwd(),'RA_Sheets/') + RA_Folder #Gets filepath of individual RA HTML Sheets
            name = response.xpath('//*[@id="titletextonly"]/text()').extract() #Extracts name of HTML Sheets
            name[0] = name[0].replace('/','-') #Replaces any slashes in HTML name to a Dash so as not to mess with pathing
            full_path = filepath+name[0] #Appends the name of the place and the filepath together
            if not os.path.exists(filepath): #If the filepath doesn't exist creates one
                os.makedirs(filepath)
            completeName = os.path.join(filepath, name[0]) #Opens file with complete name
            with open(completeName, 'wb') as f: #Opens the file
                f.write(response.body) #Writes asll the HTML to file

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
