# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonItemExporter
from ..models.plant_scraped import ScrapedPlant

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