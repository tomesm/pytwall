from datetime import datetime
from flask import Flask, url_for, render_template
from pytwall.twitterwall import TwitterWall


app = Flask(__name__)


@app.route('/')
@app.route('/<hashtag>/')
def twall(hashtag='python'):
    ptw = TwitterWall('auth.cfg')
    query = '#' + hashtag
    tweets = ptw.get_statuses(q=query, count=5, result_type='recent')

    return render_template('twall.html', tweets=tweets, hashtag=query)


@app.template_filter('time')
def better_time(text):
    """Convert the time format to a better format"""
    dt = datetime.strptime(text, '%a %b %d %H:%M:%S %z %Y')

    return dt.strftime('%c')




