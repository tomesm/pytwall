import configparser
import sys


def credentials(file):
    ''' '''
    conf = configparser.ConfigParser()
    conf.read(file)

    return conf['twitter']['api_key'], conf['twitter']['api_secret']

