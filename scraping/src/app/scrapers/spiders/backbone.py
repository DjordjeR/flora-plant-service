import scrapy


class BackboneSpider(scrapy.Spider):
    name = 'backbone'
    # allowed_domains = ['example.com']
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        self.log(f'Saved file {filename}')