from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import *
from dotenv import dotenv_values



# define schema
Base = declarative_base()

class News_Feed(Base):
    __tablename__ = "news_feedNews"
    id = Column(String, primary_key=True)
    title = Column(String)
    source = Column(String)
    description = Column(String)
    PubDate = Column(String)
