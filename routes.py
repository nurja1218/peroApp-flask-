from flask import Flask, render_template, request, redirect, url_for, make_response
from flaskwebgui import FlaskUI

from functools import wraps, update_wrapper
from datetime import datetime

# cache = Cache(config={'CACHE_TYPE': 'simple'})

app = Flask(__name__, static_url_path='/static')
# ui = FlaskUI(app)


def nocache(view):
    @wraps(view)
    def no_cache(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        response.headers['Last-Modified'] = datetime.now()
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '-1'
        return response

    return update_wrapper(no_cache, view)


@app.route('/')
@nocache
def index():
    return render_template('index.html')


@app.route('/test-1')
@nocache
def test1():
    return render_template('junyoung.html')


@app.route('/g1')
@nocache
def g1():
    return render_template('g1.html')


@app.route('/g2')
@nocache
def g2():
    return render_template('g2.html')


@app.route('/g3')
@nocache
def g3():
    return render_template('g3.html')


@app.route('/g3_1', methods=['GET', 'POST'])
@nocache
def g3_1():
    if request.method == 'POST':
        c_hand = request.form['left']
        print(c_hand)
    return render_template('g3.html')


@app.route('/g3_2', methods=['GET', 'POST'])
@nocache
def g3_2():
    if request.method == 'POST':
        c_hand = request.form['right']
        print(c_hand)
    return render_template('g3.html')


@app.route('/g4')
@nocache
def g4():
    return render_template('g4.html')


@app.route('/g4_1', methods=['GET', 'POST'])
@nocache
def g4_1():
    if request.method == 'POST':
        g3_answer = request.form['answer1']
        print(g3_answer)
    return render_template('g4.html')


@app.route('/g4_2', methods=['GET', 'POST'])
@nocache
def g4_2():
    if request.method == 'POST':
        g3_answer = request.form['answer2']
        print(g3_answer)
    return render_template('g4.html')


@app.route('/g4_3', methods=['GET', 'POST'])
@nocache
def g4_3():
    if request.method == 'POST':
        g3_answer = request.form['answer3']
        print(g3_answer)
    return render_template('g4.html')


@app.route('/g5')
@nocache
def g5():
    return render_template('g5.html')


@app.route('/g5_1', methods=['GET', 'POST'])
@nocache
def g5_1():
    if request.method == 'POST':
        g4_answer = request.form['answer1']
        print(g4_answer)
    return render_template('g5.html')


@app.route('/g5_2', methods=['GET', 'POST'])
@nocache
def g5_2():
    if request.method == 'POST':
        g4_answer = request.form['answer2']
        print(g4_answer)
    return render_template('g5.html')


@app.route('/g5_3', methods=['GET', 'POST'])
@nocache
def g5_3():
    if request.method == 'POST':
        g4_answer = request.form['answer3']
        print(g4_answer)
    return render_template('g5.html')


@app.route('/c1')
@nocache
def c1():
    return render_template('c1.html')


@app.route('/c1_1', methods=['GET', 'POST'])
@nocache
def c1_1():
    if request.method == 'POST':
        g5_answer = request.form['answer1']
        print(g5_answer)
    return render_template('c1.html')


@app.route('/c1_2', methods=['GET', 'POST'])
@nocache
def c1_2():
    if request.method == 'POST':
        g5_answer = request.form['answer2']
        print(g5_answer)
    return render_template('c1.html')


@app.route('/c1_3', methods=['GET', 'POST'])
@nocache
def c1_3():
    if request.method == 'POST':
        g5_answer = request.form['answer3']
        print(g5_answer)
    return render_template('c1.html')


@app.route('/f1')
@nocache
def f1():
    return render_template('f1.html')


@app.route('/f2')
@nocache
def f2():
    return render_template('f2.html')


@app.route('/f3')
@nocache
def f3():
    return render_template('f3.html')


@app.route('/c2')
@nocache
def c2():
    return render_template('c2.html')


@app.route('/c3')
@nocache
def c3():
    return render_template('c3.html')


@app.route('/m2-app1')
@nocache
def m1():
    return render_template('m2-app1.html')


@app.route('/m2-app2')
@nocache
def m2():
    return render_template('m2-app2.html')


@app.route('/m2-app3')
@nocache
def m3():
    return render_template('m2-app3.html')


@app.route('/m2-app4')
@nocache
def m4():
    return render_template('m2-app4.html')


@app.route('/m2-app5')
@nocache
def m5():
    return render_template('m2-app5.html')


@app.route('/m2-app6')
@nocache
def m6():
    return render_template('m2-app6.html')


@app.route('/m2-app7')
@nocache
def m7():
    return render_template('m2-app7.html')


@app.route('/m2-app8')
@nocache
def m8():
    return render_template('m2-app8.html')


@app.route('/m2-app9')
@nocache
def m9():
    return render_template('m2-app9.html')


@app.route('/m2-app10')
@nocache
def m10():
    return render_template('m2-app10.html')


if __name__ == '__main__':
    app.debug = False
    app.run(host="localhost", port="2020")
    # ui.run()
