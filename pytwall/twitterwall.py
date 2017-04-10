""" Twitter Wall
The module loads a configurable number of initial tweets, displays them and
than an infinite loop is run to check for new tweets in a configurable interval.
"""


import requests
import base64
import time


class TwitterWall:
    ''' Class for running the twitter wall logic '''

    def __init__(self, api_key, api_secret):
        ''' Class constructor initializes a session and last ID'''
        self.session = self.get_session(api_key, api_secret)
        self.last_id = 0


    def print_tweets(self, query, init_num, interval, retweets):
        ''' Infinite main loop which prints all the tweets
            :param query: A searched expression (eg. #python)
            :param init_num: Number of lodaded tweets at the beginning
            :param interval: Time interval of next queries
            :param retweets: Include retweets?
        '''
        # print init tweets
        self.print_init_tweets(query, init_num, retweets)

        for tweet in self.generate_tweets(q=query, since_id=self.last_id,
                                 count=init_num, result_type='recent'):
            if retweets or not self.is_retweet(tweet):
                print(tweet['text'])
                time.sleep(interval)


    def generate_tweets(self, **kwargs):
        ''' Infinite generator of tweets
        '''
        while True:
            yield from (self.get_statuses(**kwargs))


    def get_statuses(self, **kwargs):
        ''' Returns a list of statuses based of a given query and params
            :param kwargs: All parameters for search query
            :return: Statuses found based on given params
        '''
        tw_addr = 'https://api.twitter.com/1.1/search/tweets.json'  #twitter API address
        response = self.session.get(tw_addr, params=kwargs)
        response.raise_for_status()
        statuses = response.json()['statuses']

        if statuses:
            self.last_id = statuses[0]['id']
        return statuses


    def print_init_tweets(self, query, init_num, retweets):
        """ Prints initial tweets
        :param query:
        :param init_num:
        """
        statuses = self.get_statuses(q=query, count=init_num,
                                     result_type='recent')

        if statuses:
            self.last_id = statuses[0]['id']
        # show given number of newest tweets from 'statuses' list
        for tweet in statuses:
            if retweets or not self.is_retweet(tweet):
                print(tweet['text'])


    @classmethod
    def is_retweet(cls, tweet):
        """ Checks if the tweet is a retweet
            :param tweet:
            :return: True if the tweet is a retweet
        """
        return 'retweeted_status' in tweet or tweet['text'].startswith('RT @')


    def get_session(self, api_key, api_secret):
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
