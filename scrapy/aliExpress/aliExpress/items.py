# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AliexpressItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    searchText=scrapy.Field()
    productId=scrapy.Field()
    productUrl=scrapy.Field()
    prodName=scrapy.Field()
    price=scrapy.Field()
    sold=scrapy.Field()
    store=scrapy.Field()
    storeUrl=scrapy.Field()
    
