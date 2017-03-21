from flask import Flask, url_for, render_template
from jinja2 import Markup

# export FLASK_APP=hello.py
# export FLASK_DEBUG=1 - jen lokalne na mem pocitaci, jina knebezpeci

# name je promenna nastavena pythonem na jmeno aktualniho modulu/souboru
app = Flask(__name__) # name je jmeno modulu/souboru na disku ktery Flask hleda

# fce definujici co se stane, kdyz se dotaze na danou adresu


@app.route('/')
def hello():
    return url_for('hello_eng', username='Ma', count=80)


@app.route('/hello')
@app.route('/hello/<username>/')
@app.route('/hello/<username>/<int:count>/')
def hello_eng(username=None, count=1):
    # return 'Hello {}!' . format(username) * count
    return render_template('hello.html', name=username)


@app.template_filter('reverse_text')
def reverse_text(text):
    return reversed(text)


@app.template_filter('em')
def em(text):
    return Markup('<em>{}</em>'.format(text))
