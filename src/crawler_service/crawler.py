import requests as r
import pandas as pd
from typing import Dict, List
import xmltodict
from db_schema import NewsFeed
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils import get_db_url, get_conf


# work with sess


class Crawler:
    def __init__(self, rss_list: [Dict, List]):
        self.rss_list = rss_list
        self.df = pd.DataFrame()
        print(rss_list)

    def parse_feed(self) -> None:
        urls = self.rss_list
        df_full = pd.DataFrame()
        for n in list(range(len(urls['rss_list']))):
            response = r.get(urls['rss_list'][n]['url'])
            response_dict = xmltodict.parse(response.content)
            df = pd.DataFrame()
            df = df.append(response_dict['rss']['channel']['item'], ignore_index=True)
            df['source'] = urls['rss_list'][n]['name']
            df_full = pd.concat([df, df_full], axis=0, join='outer')
            print(df_full.columns)
        df_full = df_full.drop_duplicates(subset='guid')
        self.df = df_full

    def load_to_db(self) -> None:
        some_engine = create_engine(get_db_url())
        Session = sessionmaker(bind=some_engine)
        session = Session()
        for index, row in self.df.iterrows():
            object = NewsFeed(uid=row.guid,
                              title=row.title,
                              source=row.source,
                              description=row.description,
                              publication_date=row.pubDate)
            session.merge(object)
        session.commit()
        session.close()


if __name__ == '__main__':
    rss_list = get_conf()
    crawler = Crawler(rss_list=rss_list)
    crawler.parse_feed()
    crawler.load_to_db()
