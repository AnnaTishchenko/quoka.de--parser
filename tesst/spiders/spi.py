# -*- coding: utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import FormRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.loader.processor import TakeFirst
from scrapy.contrib.loader import XPathItemLoader
from scrapy.selector import HtmlXPathSelector
from scrapy import Request
import datetime

import re
import xml.etree.ElementTree as ET

from tesst.items import quokaItem
import scrapy


class OrphanSpider(CrawlSpider):
    Gewerblich = '0'  # 0=Nur Private    1=Nur Gewerbliche   all=all
    name = "quoka"
    num = 2
    allowed_domains = ['www.quoka.de']

    flag_first = 0  # first page flag

    def start_requests(self):
        return [FormRequest("http://www.quoka.de/immobilien/bueros-gewerbeflaechen/",
                            formdata={'classtype': 'of', 'comm': self.Gewerblich},  # filters data
                            callback=self.parse)]


    def striphtml(self, data):  # html remove function
        p = re.compile(r'<.*?>')
        return p.sub('', data)


    def parse(self, response):
        item = quokaItem()
        if not response.xpath('//*[@id="ResultListData"]/ul/li'):  # end of pages
            print 'Parsing is done!'
            return

        for sel in response.xpath('//*[@id="ResultListData"]/ul/li'):
            if self.flag_first:  # ignore *top*  position on not first  pages
                if sel.xpath("./div[4]/span/text()"):
                    continue

            url = sel.xpath('./div[2]/a/@href').extract()
            if not url:  # empty <li> pass
                continue
            url = url[0]
            url = 'http://www.quoka.de' + url

            yield scrapy.Request(url, callback=self.parseDetails, meta={'item': item})

        self.flag_first = 1
        next_page_url = 'http://www.quoka.de/qmca/search/search.html?redirect=0&catid=27_2710&pageNo=%s' % self.num
        self.num += 1 #pages counter
        #next page
        yield FormRequest(url=next_page_url, formdata={'classtype': 'of', 'comm': self.Gewerblich},
                          meta={'item': item})


    def parseDetails(self, response):

        item = response.meta['item']
        main = response.xpath('/html/body/div[3]/div[2]/div[1]/main')

        item['Anbieter_ID'] = 21
        item['Monat'] = datetime.datetime.now().strftime("%m")
        item['erzeugt_am'] = datetime.datetime.now().isoformat()
        item['Gewerblich'] = self.Gewerblich
        item['url'] = response._url
        item['Uberschrift'] = main.xpath('./div[8]/div/div[1]/h1/text()').extract()[0]
        item['PLZ'] = main.xpath('./div[8]/div/div[3]/div[2]/div[1]/strong/span/span/span[2]/text()').extract()[0]
        item['Stadt'] = main.xpath('./div[8]/div/div[3]/div[2]/div[1]/strong/span/a/span/text()').extract()[0]
        item['OBID'] = main.xpath('./div[8]/div/div[3]/div[2]/div[2]/strong[1]/text()').extract()[0].replace('\n', ' ').replace(' ', '')

        Erstellungsdatum = main.xpath('./div[8]/div/div[3]/div[2]/div[2]/text()').extract()
        for el in Erstellungsdatum:
            if el != '\n':
                item['Erstellungsdatum'] = el.replace('\n', '')
                break

        Beschreibung = main.xpath('./div[8]/div/div[3]/div[3]/div/text()').extract()[0]
        Beschreibung = self.striphtml(Beschreibung)
        Beschreibung = Beschreibung.replace('\n', ' ').replace('', '')
        item['Beschreibung'] = Beschreibung
        #item['Telefon'] = ' '
        tel = response.xpath('//*[@id="dspphone1"]/@onclick').extract() #get ajax link

        if tel:
            d = re.search("\/ajax.+\\'", tel[0])
            tel = d.group(0)
            tel = tel[0:-1] # last ' char delete
            tel = 'http://www.quoka.de' + tel
            yield scrapy.Request(tel, callback=self.parse_phone, meta={'item': item}) #load ajax link
        else:
            item['Telefon'] = ' '

        price = main.xpath('./div[8]/div/div[2]/strong/span/text()').extract() #normal price
        if not price:
            price = main.xpath('./div[8]/div/div[2]/strong/text()').extract() #VHS
        if not price: #VHB
            price = main.xpath('./div[8]/div/div[2]/div/text()').extract() #VHB
        if price:
            item['Kaufpreis'] = price[0]

        yield item

    def parse_phone(self, response): #phone gage loader

        item = response.meta['item']
        tel = response.xpath('/html/body/span/text()').extract()[0]
        if tel:
            item['Telefon'] = tel
        else:
            item['Telefon'] = ' '
        return item

