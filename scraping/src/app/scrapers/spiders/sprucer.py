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

        for e in data['alphabetList']['glossaryItems'][2:5]: #TODO: limited bcs takes too long, find distributed parsing way
            yield scrapy.Request(e['url'], callback=self.plant_parse)

    def plant_parse(self, response):
        data = response.selector.css('tbody[data-check="-1"]')
        rows = data.css('td').getall()

        item = PlantItem()
        item['common_names'] = []
        item['additional']  = {}
        additionals = dict()
        p = re.compile(r'<.*?>')
        # For each match, look-up corresponding value in dictionary
        for i in range(0, len(rows), 2):
            k = p.sub('', rows[i]).strip() 
            v = p.sub('', rows[i+1]).strip() 
            if "botanical name" in k.lower() or "latin name" in k.lower():
                item['latin_name'] = v
            elif "common name" in k.lower():
                item['common_names'].extend(re.split(r',\s?', v))
            else:
                item['additional'][k] = v
        
        self.plants.append(item)
