import yaml
from typing import Dict
import os


def get_conf(path: str = 'conf.yml') -> Dict[str, str]:
    """
    Get configs from conf file
    :param path: path to conf file
    :return: configs in Dict type
    """
    with open(path) as f:
        config = yaml.safe_load(f)
    return config


def get_db_url():
    """
    create configs dict from database data
    :return: dict with configs of databse
    """
    config_dict = {"POSTGRES_USER": os.environ["POSTGRES_USER"],
                   "POSTGRES_PASSWORD": os.environ["POSTGRES_PASSWORD"],
                   "POSTGRES_HOST": os.environ["POSTGRES_HOST"],
                   "POSTGRES_PORT": os.environ["POSTGRES_PORT"],
                   "POSTGRES_DB": os.environ["POSTGRES_DB"]}
    print(config_dict)
    return "postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}".format(
        **config_dict)
