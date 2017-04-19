from spiders.JobDataScraper import JobDataScraper
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import RAOrganizer
import pandas as pd


def main():
    RA_Table = pd.read_csv('/home/jason/Documents/Data-Collection-Tool/CraigsListScraper/CraigsListScraper/Data/RA_Mapping.csv')
    RAlist = []
    urls = []
    # for i in RA_Table.RA:
    #     i = RAOrganizer.RAAssignment(i)
    #     RAlist.append(i)
    # for i in RAlist:
    #     print(i.URL_Container)


    process = CrawlerProcess(get_project_settings())
    process.crawl('jobDataSpider')
    process.start()
    # for i in RAlist:
    #     print("RA: {}".format(i.RA))
    #     i.GetURLS()
    #     for j in i.URL_Container:
    #         print(j)
main()
