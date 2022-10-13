import yaml
from sqlalchemy import create_engine
from typing import Any, Dict
from dotenv import dotenv_values
def get_conf(
        path = '/Users/yegor/PycharmProjects/crawler/crawler/crawler/conf.yml')->Dict:
    '''
    Get configs from conf file
    :param path: path to conf file
    :return: configs in Dict type
    '''
    with open(path) as f:
        my_dict = yaml.safe_load(f)
    return my_dict

def get_db_url():
    config_dict = dotenv_values('./crawler/database.env')
    print(config_dict)
    return "postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}".format(**config_dict)

