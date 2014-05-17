from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime
from sqlalchemy.orm import backref, relation

from gis.model import DeclarativeBase
from tgext.pluggable import app_model, primary_key

class Sample(DeclarativeBase):
    __tablename__ = 'gis_samples'

    uid = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(16))

    user_id = Column(Integer, ForeignKey(primary_key(app_model.User)))
    user = relation(app_model.User)


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


