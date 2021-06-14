import scrapy
import html
import re
from ..items import *

class BushcareSpider(scrapy.Spider):
    name = 'bushcare'
    #allowed_domains = [https://roleybushcare.com.au/flora-database']
    start_urls = ['https://roleybushcare.com.au/plants_database/plantmanager.php?organisation_name=roleybushcare']

    def parse(self, response):
        data = response.selector.css('div[class="col-sm-6"]').getall()
        data = [x for x in data if any(y in x for y in ['Botanical', 'botanical', 'comments'])]

        for e in data:
            result = re.findall('<b>(.*)</b>(.*)<br>', e)
            plant_info = []
            for p in result:
                k = html.unescape(p[0]).strip().replace(u'\xa0', ' ')
                v = html.unescape(p[1]).strip().replace(u'\xa0', ' ')
                plant_info.append((k,v))

            plant_info = plant_info[:-3]
            plant_info.append(plant_info.pop(0)) #move family to back

            plant_data = PlantItem( latin_name=serialize_latin_name([plant_info[0][1], plant_info[1][1]]),
                                    common_names=serialize_common_names(plant_info[2][1]),
                                    additional=serialize_additional(plant_info[3:]))
            self.plants.append(plant_data)
