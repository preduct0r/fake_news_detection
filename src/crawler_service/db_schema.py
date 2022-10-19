from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

# define schema
Base = declarative_base()


class NewsFeed(Base):
    __tablename__ = "rss_news_feed"
    id = Column(Integer, primary_key=True)
    uid = Column(String)
    title = Column(String)
    source = Column(String)
    description = Column(String)
    publication_date = Column(String)
