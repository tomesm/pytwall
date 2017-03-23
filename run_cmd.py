import click

from pytwall.twitterwall import TwitterWall


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

    ptw = TwitterWall(config_file)
    ptw.print_tweets(query, init_num, interval, retweets)


if __name__ == '__main__':
    run()
