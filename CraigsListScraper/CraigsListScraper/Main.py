from spiders.JobDataScraper import JobDataScraper
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import RAOrganizer
import pandas as pd


def seperate_sheet(sheet):
    scraped_path = os.path.join(os.getcwd(), sheet)
    scraped_df = pd.read_csv(scraped_path)
    RAs = scraped_df['RA'].unique()
    dataframes = []
    for index, i in enumerate(RAs):
        dataframes.append(scraped_df.loc[scraped_df.RA==i])
        save_path = os.path.join(os.getcwd(), "RA_Sheets", i+".csv")
        dataframes[index].to_csv(save_path)

def main():
    process = CrawlerProcess(get_project_settings()) #Load settings for spider
    process.crawl('jobDataSpider') #Crawl with Job Data Spider
    process.start() #Start the crawling
    seperate_sheet('scraped_items.csv') #After crawling load the output csv and seperate it by RA
    #TODO Make a function that moves the outputted sheets to a dropbox folder so RAs can access



main()
