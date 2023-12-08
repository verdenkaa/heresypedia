from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session



Base = declarative_base()

class Solider(Base):
    __tablename__ = "Soliders"

    name = Column(String, primary_key=True)
    type  = Column(String)
    unit_type = Column(String)
    Parameters = Column(String)
    points = Column(Integer)
    wargear = Column(String)
    Srules = Column(String)
    Options = Column(String)
    compos = Column(String)
    d_transp = Column(String)
    Legion = Column(String)


class Weapons(Base):
    __tablename__ = "Weapons"

    name = Column(String, primary_key=True)
    Range  = Column(String)
    Str = Column(Integer)
    AP = Column(String)
    Type = Column(String)
    Class = Column(String)

class Srules(Base):
    __tablename__ = "Srules"

    name = Column(String, primary_key=True)
    ability = Column(String)
