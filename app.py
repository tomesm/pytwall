import click
import time
import pytwall as ptw


@click.command()
@click.option('--config_file', default='./auth.cfg',
                help='A path to a configuration file',
                type=click.Path(exists=True))
@click.option('--query', default='#python', help='Searched expression')
@click.option('--init_num', default=5, help='Number of lodaded tweets at the beginning')
@click.option('--interval', default=10, help='Time interval of next queries')
# @click.option('--retweets', default=False, help='Include retweets?')


def run(config_file, query, init_num, interval):
    ''' '''

    api_key, api_secret = ptw.get_credentials(config_file)
    session = ptw.get_session(api_key, api_secret)


    def get_statuses(session, **kwargs):
        ''' '''
        tw_addr = 'https://api.twitter.com/1.1/search/tweets.json'  #twitter API address
        response = session.get(tw_addr, params=kwargs)

        return response.json()['statuses']


    statuses = get_statuses(session, q=query)
    # show given number of newest tweets from 'statuses' list

    for tweet in statuses[:init_num]:
        print(tweet['text'])
    # get last tweet id
    last_id = statuses[0]['id']

    while True:
        time.sleep(interval)
        # check if something is changed
        new_statuses = get_statuses(session, q=query, since_id=last_id)

        if statuses and statuses != new_statuses:
            # new statuses detected
            for tweet in statuses:
                print(tweet['text'])

            last_id = statuses[0]['id']

        # copy new list into old list
        statuses = new_statuses[:]
        new_statuses = []


if __name__ == '__main__':
    run()
