from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base


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


class Weapons(Base):
    __tablename__ = "Weapons"

    name = Column(String, primary_key=True)
    range  = Column(String)
    str = Column(Integer)
    AP = Column(String)
    Type = Column(String)
    Class = Column(String)

