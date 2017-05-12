import betamax
import configparser
import pytest
import pytwall



@pytest.fixture
def client(betamax_session):
    key, secret = get_credentials('auth.cfg')
    betamax_session.headers.update({'accept-encoding': 'identity'})
    return pytwall.twitterwall.TwitterWall(key, secret, session=betamax_session)


def test_twitter(client):
    twitter = client
