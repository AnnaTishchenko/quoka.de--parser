from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
Base = declarative_base()


class itemm(Base):
    __tablename__ = 'itemm'
    #__table_args__ = (UniqueConstraint('url'),)
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)

    OBID = Column(String(10))
    erzeugt_am = Column(DateTime, default=datetime.datetime.utcnow)
    Anbieter_ID = Column(String(8))
    Stadt = Column(String(150))
    PLZ = Column(String(8))
    Uberschrift= Column(String(500))
    Beschreibung = Column(String(1500))
    Kaufpreis = Column(String(8))
    Monat = Column(String(8))
    url = Column(String(1000))
    Telefon = Column(String(100))
    Erstellungsdatum= Column(String(12))
    Gewerblich = Column(String(8))


engine = create_engine('sqlite:///quoka.db')

Base.metadata.create_all(engine)
























# from sqlalchemy import Column, String, Integer, DateTime
# from connection import Base
#
# class AllData(Base):
#     __tablename__ = 'Quoka'
#
#     id = Column(Integer, primary_key=True)
#     Beschreibung = Column(String(1000))
#     url = Column(String(1000))
#     Stadt = Column(String(1000))
#
#     def __init__(self, id=None, Beschreibung=None, url=None, Stadt=None):
#         self.id = 1
#         self.Beschreibung = Beschreibung
#         self.url = url
#         self.Stadt = Stadt
#
#     def __repr__(self):
#         return "<AllData: id='%d', Beschreibung='%s', url='%s', Stadt='%s'>" % (self.id, self.Beschreibung, self.url, self.Stadt)



