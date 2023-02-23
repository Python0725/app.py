from flask import Flask
from markupsafe import escape

app = Flask(__name__)


@app.route('/user/<name>')
def user_page(name):
    return f'User: {escape(name)}'


@app.route('/')
def hello():
    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'


@app.route('/index')
def hello2():
    return '<h1>Hello2 Totoro!</h1><img src="http://helloflask.com/totoro.gif">'


@app.route('/home')
def hello3():
    return '<h1>Hello3 Totoro!</h1><img src="http://helloflask.com/totoro.gif">'
