# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

def serialize_common_name(value):
    names = value.split(',')
    names = [x.strip() for x in names]
    return names[0]

def serialize_latin_name(value):
    lname = value[0].capitalize()
    for i in range(1, len(value)):
        lname += " " + value[i].lower()
    return lname

def serialize_additional(value):
    gen = generate_item(value)
    for e in value:
        gen[e[0]] = e[1]
    return gen

def generate_item(additionals):
    item = scrapy.Item()
    for f in additionals:
        item.fields[f[0]] = scrapy.Field()
    return item

class PlantItem(scrapy.Item):
    # define the fields for your item here like:
    latin_name      = scrapy.Field(serializer=serialize_latin_name)
    common_name     = scrapy.Field(serializer=serialize_common_name)
    additional      = scrapy.Field(serializer=serialize_additional)