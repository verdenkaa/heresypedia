from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the model
Base = declarative_base()


class Solider(Base):
    __tablename__ = "Soliders"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type  = Column(String)


# Create an SQLite database
engine = create_engine("sqlite:///data.db")

# Create tables
Base.metadata.create_all(engine)