import click
import pytwall as ptw


@click.command()
@click.option('--config_file', default='./auth.cfg',
                help='A path to a configuration file',
                type=click.Path(exists=True))
@click.option('--query', default='#python', help='Searched expression')
@click.option('--init_num', default=5, help='Number of lodaded tweets at the beginning')
@click.option('--interval', default=10, help='Time interval of next queries')
@click.option('--retweets', default=False, help='Include retweets?')


def main(config_file, query, init_num, interval, retweets):
    ''' Run terminal Twitter Wall '''
    ptw.run(config_file, query, init_num, interval, retweets)


if __name__ == '__main__':
    main()
