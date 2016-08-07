# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'


class quokaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Anbieter_ID = Field()
    Erstellungsdatum = Field()
    Kaufpreis = Field()
    Monat = Field()
    Boersen_ID = Field()
    OBID = Field()
    erzeugt_am = Field()
    Stadt = Field()
    PLZ = Field()
    Uberschrift = Field()
    Beschreibung = Field()
    url = Field()
    Telefon = Field()
    Gewerblich = Field()

