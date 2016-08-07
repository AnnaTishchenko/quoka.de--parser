# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import  Base, itemm, engine
import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logging.debug('A debug message!')


class TesstPipeline(object):
    session=0


    def __init__(self):


        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        global session
        session = DBSession()
        pass

    #def open_spider(self, spider):


    def process_item(self, item, spider):


        # create a new SQL Alchemy object and add to the db session
        todb = itemm(OBID = item['OBID'],
                     Anbieter_ID = item['Anbieter_ID'],
                     Stadt = item['Stadt'],
                     PLZ=item['PLZ'],
                     Uberschrift=item['Uberschrift'],
                     Beschreibung=item['Beschreibung'],
                     Kaufpreis=item['Kaufpreis'],
                     Monat = item['Monat'],
                     url = item['url'],
                     Telefon= item['Telefon'],
                     Erstellungsdatum=item['Erstellungsdatum'],
                     Gewerblich = item['Gewerblich'])

        session.add(todb)
        session.commit()

        return item


    def close_spider(self,spider):
        pass
