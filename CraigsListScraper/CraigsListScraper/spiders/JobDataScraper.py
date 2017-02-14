import scrapy
from .. import items
import csv

class CraigsListDistrictSpider(scrapy.Spider):
    name = "districtURLSpider"
    start_urls = starting