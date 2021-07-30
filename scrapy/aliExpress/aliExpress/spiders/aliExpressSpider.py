#-*- coding=utf-8 -*-
import scrapy
import time
import re
import json
from jsonpath import jsonpath
from aliExpress.items import AliexpressItem
from scrapy import Request


class AliexpressspiderSpider(scrapy.Spider):
    name = 'aliExpressSpider'
    allowed_domains = ['aliexpress.com']
    #searchText='ewelink'
    #start_urls = ['http://aliexpress.com/']
    start_urls = ['https://www.aliexpress.com/wholesale?trafficChannel=main&d=y&CatId=0&SearchText=']
    tmp='&ltype=wholesale&SortType=default&page='

    # 对请求的返回进行处理的配置
    meta = {
        'dont_redirect': True,  # 禁止网页重定向
        'handle_httpstatus_list': [301, 302]  # 对哪些异常返回进行处理
    }
    #simple of different url:https://www.aliexpress.com/wholesale?trafficChannel=main&d=y&CatId=0&SearchText=ewelink&ltype=wholesale&SortType=default&page=1
    #simple of good url:https://www.aliexpress.com/item/1005002537788040.html

    def start_requests(self):
        key=self.settings.get('KEY_WORDS')
        url=self.start_urls[0]+key[0]
        yield Request(url=url,callback=self.parse,meta=self.meta)

    def parse(self, response):
        #pass
        content=scrapy.Selector(response)
        selector=content.xpath('/html/body/script[@type="text/javascript"]/text()')[0].extract()
        pattern=re.compile(r'{"mods":.*};')
        prodStr=re.search(pattern,selector).group()
        prodDict=json.loads(prodStr.rstrip(';'))
        #items=[]

        lProductId=jsonpath(prodDict, '$..content[*].productId') 
        lProdName=jsonpath(prodDict,'$..content[*].title')
        lPrice=jsonpath(prodDict,'$..content[*].prices.salePrice')
        lSold=jsonpath(prodDict,'$..content[*].trade')
        lStore=jsonpath(prodDict,'$..content[*].store')

        for i in range(0,len(lProdName)):
            item=AliexpressItem()
            item['searchText']=content.xpath('//input[@name="SearchText"]/@value').extract()[0]
            item['productId']=lProductId[i]
            item['productUrl']='https://www.aliexpress.com/item/'+str(lProductId[i])+'.html'
            item['prodName']=lProdName[i].get('displayTitle')  
            item['price']=lPrice[i].get('formattedPrice')
            try:
                item['sold']=lSold[i].get('tradeDesc')
                item['store']=lStore[i].get('storeName')
                item['storeUrl']=lStore[i].get('storeUrl').lstrip('//')
            except IndexError:
                item['sold']=0
                item['store']='None'
                item['storeUrl']='None'
            yield item
            
        #page get
        p1=re.compile(r'"maxPage":\d*')
        pageInfo=re.search(p1,selector).group()
        totalPage=pageInfo.split(':')
        key=self.settings.get('KEY_WORDS')
        if pageInfo:
            for page in range(2,int(totalPage[1])+1):
                url=self.start_urls[0]+key[0]+self.tmp+str(page)
                yield Request(url=url,callback=self.sub_parse,meta=self.meta)
                
    def sub_parse(self,response):
        content=scrapy.Selector(response)
        selector=content.xpath('/html/body/script[@type="text/javascript"]/text()')[0].extract()
        pattern=re.compile(r'{"mods":.*};')
        prodObj=re.search(pattern,selector)
        if prodObj:
            prodStr=prodObj.group()
            prodDict=json.loads(prodStr.rstrip(';'))

            lProductId=jsonpath(prodDict, '$..content[*].productId') 
            lProdName=jsonpath(prodDict,'$..content[*].title')
            lPrice=jsonpath(prodDict,'$..content[*].prices.salePrice')
            lSold=jsonpath(prodDict,'$..content[*].trade')
            lStore=jsonpath(prodDict,'$..content[*].store')

            for i in range(0,len(lProdName)):
                item=AliexpressItem()
                item['searchText']=content.xpath('//input[@name="SearchText"]/@value').extract()[0]
                item['productId']=lProductId[i]
                item['productUrl']='https://www.aliexpress.com/item/'+str(lProductId[i])+'.html'
                item['prodName']=lProdName[i].get('displayTitle')  
                item['price']=lPrice[i].get('formattedPrice')
                try:
                    item['sold']=lSold[i].get('tradeDesc')
                    item['store']=lStore[i].get('storeName')
                    item['storeUrl']=lStore[i].get('storeUrl').lstrip('//')
                except IndexError:
                    item['sold']=0
                    item['store']='None'
                    item['storeUrl']='None'
                yield item
        else:
            return