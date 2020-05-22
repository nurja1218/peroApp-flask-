from flask import Flask, render_template, request, redirect, url_for
from flask_caching import Cache
from flaskwebgui import FlaskUI

# cache = Cache(config={'CACHE_TYPE': 'simple'})

app = Flask(__name__)
ui = FlaskUI(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/g_question1')
def g1():
    return render_template('g1.html')


@app.route('/g2')
def g2():
    return render_template('g2.html')


@app.route('/g3')
def g3():
    return render_template('g3.html')


@app.route('/g4')
def g4():
    return render_template('g4.html')


@app.route('/g5')
def g5():
    return render_template('g5.html')


@app.route('/f1')
def f1():
    return render_template('f1.html')


@app.route('/f2')
def f2():
    return render_template('f2.html')


@app.route('/f3')
def f3():
    return render_template('f3.html')


@app.route('/c1')
def c1():
    return render_template('c1.html')


@app.route('/c2')
def c2():
    return render_template('c2.html')


@app.route('/c3')
def c3():
    return render_template('c3.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host="127.0.0.1", port="1234")
    # ui.run()
