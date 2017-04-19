from spiders.JobDataScraper import JobDataScraper
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import RAOrganizer
import pandas as pd


def main():

    process = CrawlerProcess(get_project_settings())
    process.crawl('jobDataSpider')
    process.start()
main()
