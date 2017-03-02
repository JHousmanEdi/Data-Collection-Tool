# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from __future__ import absolute_import
from scrapy.item import Item, Field


class CraigsListRegion(Item):
    state = Field()
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


class JobInfoGood(Item):
    CL_ID = Field()
    Month = Field()
    Day = Field()
    State = Field()
    Occupation = Field()
    ToAddress = Field()
    WordResume = Field()
    Company = Field()
    CompanyDescription = Field()
    EmailSubject = Field()
    City = Field()
    url = Field()
    RA = Field()


class JobInfoBad(Item):
    City = Field()
    CL_ID = Field()
    Month_Posted = Field()
    Day_Posted = Field()
    Reason = Field()
    ManagerialSupervisor = Field()
    AlreadyApplied = Field()
    BilingualRequirement = Field()
