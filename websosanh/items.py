# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LazadaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    regular_price = scrapy.Field()
    sale_price = scrapy.Field()
    product_saving = scrapy.Field()
    url = scrapy.Field()
    image_url = scrapy.Field()

class CellphonesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    category = scrapy.Field()
    regular_price = scrapy.Field()
    sale_price = scrapy.Field()
    url = scrapy.Field()
    image_url = scrapy.Field()

class AdayroiItem(scrapy.Item):
    title = scrapy.Field()
    category = scrapy.Field()
    regular_price = scrapy.Field()
    sale_price = scrapy.Field()
    product_saving = scrapy.Field()
    url = scrapy.Field()
    image_url = scrapy.Field()
