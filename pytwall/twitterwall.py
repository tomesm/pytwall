import configparser
import requests
import base64
import time


class TwitterWall:
    ''' Class for running the twitter wall logic '''

    def __init__(self, config_file):
        ''' Class constructor initializes a session and last ID'''
        self.api_key, self.api_secret = self.get_credentials(config_file)
        self.session = self.get_session(self.api_key, self.api_secret)
        self.last_id = 0


    def generate_tweets(self, query, init_num, interval, retweets):
        ''' Infinite main loop which prints all the tweets

            :param query: A searched expression (eg. #python)
            :param init_num: Number of lodaded tweets at the beginning
            :param interval: Time interval of next queries
            :param retweets: Include retweets?
        '''

        # print init number of tweets
        statuses = self.get_statuses(q=query)
        # show given number of newest tweets from 'statuses' list
        for tweet in statuses[:init_num]:
            if retweets or not self.is_retweet(tweet):
                print(tweet['text'])
        # get last tweet id
        self.last_id = statuses[0]['id']

        # TODO: break down into more functions - replace FOR loops with generators
        while True:
            time.sleep(interval)
            # check if something is changed
            new_statuses = self.get_statuses(q=query, since_id=self.last_id)

            if new_statuses and statuses != new_statuses:
                # new statuses detected
                for tweet in new_statuses:
                    if retweets or not self.is_retweet(tweet):
                        print(tweet['text'])

                self.last_id = new_statuses[0]['id']

            # copy new list into old list
            statuses = new_statuses[:]
            new_statuses = []


    def get_statuses(self, **kwargs):
        ''' Returns a list of statuses based of a given query

            :param session: An established instance session
            :param kwargs: All parameters for search query
            :return: Statuses found based on given params
        '''
        tw_addr = 'https://api.twitter.com/1.1/search/tweets.json'  #twitter API address
        response = self.session.get(tw_addr, params=kwargs)

        return response.json()['statuses']


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


    def get_credentials(self, file):
        """ Derives credentials form an auth file

            :param file: a config file with auth keys
            :return: config list with twitter credentials
        """
        config = configparser.ConfigParser()
        config.read(file)

        return config['twitter']['api_key'], config['twitter']['api_secret']

