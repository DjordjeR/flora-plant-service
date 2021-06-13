from ..items import ZipfileItem
import scrapy


class MidwestHerbariaSpider(scrapy.Spider):
    name = 'midwest_herbaria'
    start_urls = ['https://nansh.org/portal/content/dwca/ARCH-herbarium_DwC-A.zip']
    custom_settings= {
        "ITEM_PIPELINES": {
            'scrapy.pipelines.files.FilesPipeline': 1,
            'app.scrapers.pipelines.DWCADownloadedPipeline': 2
            },
        "FILES_STORE": 'tmp/scrapyDownloaded'
        }

    def parse(self, response):
        self.log(response.url)
        item = ZipfileItem()
        item['file_urls'] = [response.url]
        yield item
