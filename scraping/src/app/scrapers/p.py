import scrapy

class Human(scrapy.Item):
    sex = scrapy.Field()
    physical = scrapy.Field()
    full_name = scrapy.Field()

class Physical(scrapy.Item):
    height = scrapy.Field()
    weight = scrapy.Field()

p = Physical()
p['height'] = 180
p['weight'] = 80
h = Human()
h['physical'] = p
h['sex'] = 'yes'
print(h)