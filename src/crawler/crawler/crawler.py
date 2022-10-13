import requests as r
import pandas as pd
from typing import Dict, List
import xmltodict
from fake_news_detection.src.crawler import News_Feed
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fake_news_detection.src.crawler import get_db_url
from fake_news_detection.src.crawler import get_conf



# work with sess



class Crawler:
    def __init__(self, rss_list:[Dict,List]):
        self.rss_list = rss_list
        self.df = pd.DataFrame()
        print(rss_list)

    def parse_feed(self):
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

    def load_to_db(self):
        some_engine = create_engine(get_db_url())
        Session = sessionmaker(bind=some_engine)
        session = Session()
        # inst = inspect(News_Feed)
        objects = []
        for index, row in self.df.iterrows():
            objects.append(News_Feed(id = row.guid,
                                title = row.title,
                                source = row.source,
                                description = row.description,
                                PubDate = row.pubDate))
        session.bulk_save_objects(objects)
        session.commit()
        # session.execute(table_addresses.insert().values(name='Joe', age=20))
        # attr_names = [c_attr.key for c_attr in inst.mapper.column_attrs]
        # cursor = conn.cursor()
        # cursor.execute("INSERT INTO news_feedNews () VALUES(%s, %s, %s)", (v1, v2, v3))
        # conn.commit()  # <- We MUST commit to reflect the inserted data
        # cursor.close()
        # conn.close()

def main():
    rss_list = get_conf()
    crawler = Crawler(rss_list = rss_list)
    crawler.parse_feed()
    crawler.load_to_db()

