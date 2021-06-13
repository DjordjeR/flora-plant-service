import scrapy
import re
from ..items import *
import json

class SprucerSpider(scrapy.Spider):
    name = 'sprucer'
    #allowed_domains = ['https://www.thespruce.com/plants-a-to-z-5116344']
    start_urls=['https://www.thespruce.com/plants-a-to-z-5116344']
    custom_settings={
        'ROBOTSTXT_OBEY': False,
        'COOKIES_ENABLED': False
    }

    def parse(self, response):
        data = re.search(rb'var newData = (.*);', response.body)
        data = json.loads(data.group(1))
        self.log('*'*100)
        self.log(len(data['alphabetList']['glossaryItems']))
        self.log('*'*100)