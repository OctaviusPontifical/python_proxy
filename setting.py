import configparser
import os


def get_param(name):
    conf  = os.environ.get(name)
    if conf:
        return conf
    else :
        config = configparser.ConfigParser()
        try:
            config.read("config.ini")
            return config['SETTING'][name]
        except Exception :
            config.read(os.environ.get('PROXY_PATH_SETTING'))
            return config['SETTING'][name]
