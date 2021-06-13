# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

def serialize_common_names(value):
    names = value.split(',')
    names = [x.strip() for x in names]
    return names

def serialize_latin_name(value):
    if "<font" in value[0]:
        lname = value[0].split('<font')[0].strip().capitalize()
    else:
        lname = value[0].capitalize()

    for i in range(1, len(value)):
        if "<font" in value[i]:
            lname += " " + value[i].split('<font')[0].lower()
        else:
            lname += " " + value[i].lower()
    return lname

def serialize_additional(value):
    additionals = {} 
    for e in value:
        additionals[e[0]] = e[1]
    return additionals

def generate_item(additionals):
    item = scrapy.Item()
    for f in additionals:
        item.fields[f[0]] = scrapy.Field()
    return item

class PlantItem(scrapy.Item):
    # define the fields for your item here like:
    latin_name      = scrapy.Field()
    common_names    = scrapy.Field()
    additional      = scrapy.Field()

class ZipfileItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()