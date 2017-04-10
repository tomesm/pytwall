import click
import configparser

from .twitterwall import TwitterWall

def get_credentials(file):
    """ Derives credentials form an auth file
        :param file: a config file with auth keys
        :return: config list with twitter credentials
    """
    config = configparser.ConfigParser()
    config.read(file)

    return config['twitter']['api_key'], config['twitter']['api_secret']


@click.command()
@click.option('--config_file', default='./auth.cfg',
                help='A path to a configuration file',
                type=click.Path(exists=True))
@click.option('--query', default='#python', help='Searched expression, (eg. #python)')
@click.option('--init_num', default=5, help='Number of lodaded tweets at the beginning')
@click.option('--interval', default=10, help='Time interval of next queries')
@click.option('--retweets', default=False, help='Include retweets?')


def run(config_file, query, init_num, interval, retweets):
    ''' Run terminal Twitter Wall '''

    ptw = TwitterWall(*get_credentials(config_file))
    ptw.print_tweets(query, init_num, interval, retweets)
