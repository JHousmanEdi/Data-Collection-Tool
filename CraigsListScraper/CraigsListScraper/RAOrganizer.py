from collections import  defaultdict
from csv import DictReader
import pandas as pd


def getRATable():
    columnwise_table = defaultdict(list)
    with open('/home/jason/Documents/Data-Collection-Tool/CraigsListScraper/CraigsListScraper/Data/RA_Mapping.csv'
,'rU') as f:
        reader = DictReader(f)
        for row in reader:
            for col,dat in row.items():
                columnwise_table[col].append(dat)
    return columnwise_table

def getURLTable():
    pd.read_csv('/home/jason/Documents/Data-Collection-Tool/CraigsListScraper/CraigsListScraper/Data/all_URLS_Indexed.csv')

def mapURLRA():
    URL_table = pd.read_csv('/home/jason/Documents/Data-Collection-Tool/CraigsListScraper/CraigsListScraper/Data/all_URLS_Indexed.csv')
    RA_Table = pd.read_csv('/home/jason/Documents/Data-Collection-Tool/CraigsListScraper/CraigsListScraper/Data/RA_Mapping.csv')
