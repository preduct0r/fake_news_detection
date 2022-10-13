import yaml
from sqlalchemy import create_engine
from typing import Any, Dict
from dotenv import dotenv_values
def get_conf(
        path = './src/crawler/crawler/conf.yml')->Dict:
    '''
    Get configs from conf file
    :param path: path to conf file
    :return: configs in Dict type
    '''
    with open(path) as f:
        my_dict = yaml.safe_load(f)
    return my_dict

def get_db_url():
    '''
    create configs dict from database data
    :return: dict with configs of databse
    '''
    config_dict = dotenv_values('./src/crawler/db/database.env')
    print(config_dict)
    return "postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}".format(**config_dict)

