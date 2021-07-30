# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import codecs
import csv
import time


class AliexpressPipeline:
    def process_item(self, item, spider):
        curDate=time.strftime('%Y%m%d',time.localtime())
        fileName='/pythonProject/scrapy/aliExpress/aliExpress_goods_'+item['searchText']+'_'+curDate+'.txt'
        with codecs.open(fileName, 'a+', encoding='utf-8') as fp:
            fp.write('%s|%s|%s|%s|%s|%s|%s|%s\n'%(item['searchText'],item['productId'],item['prodName'],item['price'],item['sold'],item['store'],item['storeUrl'],item['productUrl']))
        return item