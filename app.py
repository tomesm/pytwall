import click
import twcredentials
import twsessions

@click.command()
@click.option('--config_file', default='./auth.cfg',
                help='A path to a configuration file',
                type=click.Path(exists=True))
@click.option('--query', default='#python', help='Searched expression')
# @click.option('--init_num', default='10', help='Number of lodaded tweets at the beginning')
# @click.option('--interval', default='5', help='Time interval of next queries')
# @click.option('--retweets', default=False, help='Include retweets?')



def run(config_file, query):
    ''' '''
    api_key, api_secret = twcredentials.credentials(config_file)
    session = twsessions.get_tw_session(api_key, api_secret)
    response = session.get('https://api.twitter.com/1.1/search/tweets.json',
                            params={'q' : query})

    statuses = response.json()['statuses']

    for tweet in statuses:
        print(tweet['text'])


if __name__ == '__main__':
    run()


