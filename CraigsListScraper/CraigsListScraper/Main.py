from spiders.JobDataScraper import JobDataScraper
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import RAOrganizer
import pandas as pd


def main():
    RA_Table = pd.read_csv('/home/jason/Documents/Data-Collection-Tool/CraigsListScraper/CraigsListScraper/Data/RA_Mapping.csv')
    RAlist = []
    for i in RA_Table.RA:
        i = RAOrganizer.RAAssignment(i)
        RAlist.append(i)
    process = CrawlerProcess(get_project_settings())
    for i in RAlist:
        process.crawl('jobDataSpider', RA = i.RA)
    process.start()
main()
