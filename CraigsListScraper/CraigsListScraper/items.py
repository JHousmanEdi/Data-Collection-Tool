# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from __future__ import absolute_import
from scrapy.item import Item, Field


class CraigsListRegion(Item):
    name = Field()
    url = Field()


class CraigsListDistrict(Item):
    region = Field()
    district = Field()
    url = Field()

class CraigsListJobs(Item):
    region = Field()
    district = Field()
    job_name = Field()
    url = Field()