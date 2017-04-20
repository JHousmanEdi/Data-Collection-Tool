# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name         = 'CraigsListScraper',
    version      = '1.0',
    packages     = find_packages(),
    package_data={
        'CraigsListScraper': ['Data/*.csv', 'Data/*.csv', '*.csv']
    },
    entry_points = {'scrapy': ['settings = CraigsListScraper.settings']},
    zip_safe=False,
)
