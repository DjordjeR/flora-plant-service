# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import spiders
from scrapy.exporters import JsonItemExporter
from ..models.plant_scraped import ScrapedPlant
from dwca.read import DwCAReader
from dwca.darwincore.utils import qualname as qn
from .items import PlantItem
import os

class DWCADownloadedPipeline:
    async def process_item(self, item, spider):
        fPath = os.path.join('tmp/scrapyDownloaded', item['files'][0]['path'])
        print(fPath)
        interesting_data = ['recordedBy','family', 'recordedDate', 'order', 'class', 'phylum', 'kingdom', 'habitat']
        with DwCAReader(fPath) as dwca:
            print('*'*100)
            # loop through entries and add to itemslist
            print(len(dwca.rows))
            print('+'*100)
            for e in dwca.rows:
                if not len(e.data.get('http://rs.tdwg.org/dwc/terms/scientificName')):
                    continue
                curr_item = PlantItem()
                curr_item['common_names'] = []
                additionals = {}
                for k,v in e.data.items():
                    if len(v) and 'http://rs.tdwg.org/dwc/terms/vernacularName' == k:
                        curr_item['common_names'].append(v)                        
                    if 'http://rs.tdwg.org/dwc/terms/scientificName' == k:
                        curr_item['latin_name'] = v
                    elif len(v):
                        for ik in interesting_data:
                            if 'http://rs.tdwg.org/dwc/terms/'+ik == k:
                                additionals[ik] = v
                curr_item['additional'] = additionals
                spider.plants.append(curr_item)
        print('*'*100)
        return item