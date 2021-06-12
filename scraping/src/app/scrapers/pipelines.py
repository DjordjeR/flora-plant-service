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


class ScrapersPipeline:
    def open_spider(self, spider):
        print('*'*100)
        print('OPENING')
        '''
        open('test.json', 'w').close()
        self.fd = open('test.json', 'ab')
        self.exporter = JsonItemExporter(self.fd)
        self.exporter.start_exporting()
        '''

    def close_spider(self, spider):
        print('*'*100)
        print('CLSOING')
        '''
        self.exporter.finish_exporting()
        self.fd.close()
        spider.clo
        '''

    async def process_item(self, item, spider):
        print('ADD TO DB HERE')
        #self.exporter.export_item(item)
        spider.plants.append(item)
        # check postgres db conn
        #sp = ScrapedPlant(latin_name=item['latin_name'], common_name=item['common_name'], additional=item['additional'])
        #await save_to_db(sp)
        return item


class DWCADownloadedPipeline:
    async def process_item(self, item, spider):
        crd = os.path.dirname(os.path.realpath(__file__))
        fPath = os.path.join(os.path.join(crd, 'filesDL'), item['files'][0]['path'])
        print(fPath)
        interesting_data = ['recordedBy','family', 'recordedDate', 'order', 'class', 'phylum', 'kingdom', 'habitat']
        with DwCAReader(fPath) as dwca:
            print('*'*100)
            # loop through entries and add to itemslist
            print(len(dwca.rows))
            print('+'*100)
            for e in dwca.rows:
                curr_item = PlantItem()
                additionals = {}
                for k,v in e.data.items():
                    if 'vernacularName' in k and len(v):
                        curr_item['common_names'] = v
                    elif 'scientificName' in k and len(v):
                        curr_item['latin_name'] = v
                    else:#if any(map(k.__contains__, interesting_data)):
                        additionals[k] = v
                curr_item['additional'] = additionals
                spider.plants.append(curr_item)

        print('*'*100)
        return item