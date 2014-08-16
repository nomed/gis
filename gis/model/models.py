from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime
from sqlalchemy.orm import backref, relation

from gis.model import DeclarativeBase
from tgext.pluggable import app_model, primary_key


class Hotspot(DeclarativeBase):
    __tablename__ = 'hotspot'

    #{ Columns

    hotspot_id = Column(Integer, primary_key=True)
    hotspot_alias = Column(Unicode(50), unique=True)

    #}

class Hotspotlog(DeclarativeBase):
    __tablename__ = 'hotspot_log'

    #{ Columns

    hotspotlog_id = Column(Integer, primary_key=True)
    hotspot_id = Column(Integer, ForeignKey(Hotspot.hotspot_id))
    hotspot = relation('Hotspot', backref='logs')
    email = Column(Unicode(50))
    date = Column(DateTime)
    name = Column(Unicode(50))
    surname = Column(Unicode(50))


    #}

class Crm(DeclarativeBase):
    __tablename__ = 'crm'

    #{ Columns

    crm_id = Column(Integer, primary_key=True)
    leid = Column(Unicode(32),unique=True)
    euid = Column(Unicode(32), unique=True)
    email = Column(Unicode(50), unique=True)
    fname = Column(Unicode(50))
    lname = Column(Unicode(50))
    company = Column(Unicode(50))
    address_addr1 = Column(Unicode(50))
    address_addr2 = Column(Unicode(50))
    address_city = Column(Unicode(50))
    address_state = Column(Unicode(50))
    address_zip=Column(Unicode(16))
    address_country=Column(Unicode(32))
    birthday_day = Column(Integer)
    birthday_month = Column(Integer)
    gender = Column(Unicode(1))
    source = Column(Unicode(32))



    #}


