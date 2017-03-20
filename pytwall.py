import configparser
import sys
import requests
import base64
import time


def run(config_file, query, init_num, interval, retweets):
    ''' Infinite main loop

        :param config_file:
        :param query:
        :param init_num:
        :param interval:
    '''
    api_key, api_secret = get_credentials(config_file)
    session = get_session(api_key, api_secret)

    statuses = get_statuses(session, q=query)
    # show given number of newest tweets from 'statuses' list
    for tweet in statuses[:init_num]:
        if retweets or not is_retweet(tweet):
            print(tweet['text'])

    # get last tweet id
    last_id = statuses[0]['id']

    # TODO: break down into more functions - replace FOR loops with generators
    while True:
        time.sleep(interval)
        # check if something is changed
        new_statuses = get_statuses(session, q=query, since_id=last_id)

        if statuses and statuses != new_statuses:
            # new statuses detected
            for tweet in statuses:
                if retweets or not is_retweet(tweet):
                    print(tweet['text'])

            last_id = statuses[0]['id']

        # copy new list into old list
        statuses = new_statuses[:]
        new_statuses = []



def get_statuses(session, **kwargs):
    ''' Returns a list of statuses based of a given query

        :param session:
        :param kwargs:
        :return:
    '''
    tw_addr = 'https://api.twitter.com/1.1/search/tweets.json'  #twitter API address
    response = session.get(tw_addr, params=kwargs)

    return response.json()['statuses']


def is_retweet(tweet):
    """ Checks if the tweet is a retweet

        :param tweet:
        :return: True if retweet
    """

    return 'retweeted_status' in tweet or tweet['text'].startswith('RT @')



def get_session(api_key, api_secret):
    """ Gets sessions

        :param api_key:
        :param api_secret:
        :return: established session
    """
    session = requests.Session()
    secret = '{}:{}'.format(api_key, api_secret)
    secret64 = base64.b64encode(secret.encode('ascii')).decode('ascii')

    headers = {
        'Authorization': 'Basic {}'.format(secret64),
        'Host': 'api.twitter.com',
    }

    request = session.post('https://api.twitter.com/oauth2/token',
                        headers=headers,
                        data={'grant_type': 'client_credentials'})

    bearer_token = request.json()['access_token']

    def bearer_auth(req):
        req.headers['Authorization'] = 'Bearer ' + bearer_token

        return req

    session.auth = bearer_auth

    return session


def get_credentials(file):
    """ Derives credentials form an auth file

        :param file:
        :return: config list with twitter credentials
    """
    config = configparser.ConfigParser()
    config.read(file)

    return config['twitter']['api_key'], config['twitter']['api_secret']

