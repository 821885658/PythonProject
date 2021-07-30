#-*-coding:utf-8 -*-
from scrapy.conf import settings
from scrapy.contrib.exporter import CsvItemExporter

#自定义的CSV输出
class AliCsvItemExpoter(CsvItemExporter):
    def __init__(self,*agrs,**kwagrs):
        delimiter=settings.get("CSV_DELIMITER")
        kwagrs['delimiter']=delimiter
        fields_to_export=settings.get('FIELDS_TO_EXPORT',[])
        if fields_to_export:
            kwagrs['fields_to_export'] = fields_to_export
        super(AliCsvItemExpoter,self).__init__(*agrs,**kwagrs)