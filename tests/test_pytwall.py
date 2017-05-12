import betamax
import configparser
import pytest
import pytwall
import os

def get_credentials(file):
    """ Derives credentials form an auth file
        :param file: a config file with auth keys
        :return: config list with twitter credentials
    """
    config = configparser.ConfigParser()
    config.read(file)

    return config['twitter']['api_key'], config['twitter']['api_secret']

with betamax.Betamax.configure() as config:

    config.cassette_library_dir = 'tests/fixtures/cassettes'

    if 'API_KEY' in os.environ and 'API_SECRET' in os.environ:
        config.default_cassette_options['record_mode'] = 'all'
    else:
        config.default_cassette_options['record_mode'] = 'none'

@pytest.fixture
def client(betamax_session):

    betamax_session.headers.update({'accept-encoding': 'identity'})
    key = os.environ.get('API_KEY', 'fake_key')
    secret = os.environ.get('API_SECRET', 'fake_secret')
    return pytwall.twitterwall.TwitterWall(key, secret, session=betamax_session)


def test_twitter(client):
    twitter = client
