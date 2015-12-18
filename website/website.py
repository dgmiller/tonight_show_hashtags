from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
import sqlite3

import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'..' ))
from tonight import streamer

stream = streamer.get_driver()

DATABASE = '/tmp/test.db'
DEBUG = True
SECRET_KEY = 'whocares'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask("website")
app.config.from_object('website')

@app.before_request
def before_request() :

    if ((not 'logged_in' in session or not session['logged_in']) and request.endpoint != 'login') :
        return redirect(url_for('login'))

@app.route('/scraper', methods=['GET'])
def scraper() :
    if (request.method == 'GET' and 'test' in request.args) :
        print(request.args['test'])
    message = None
    return render_template('scraper.html')

@app.route('/') 
def main_page():
    return redirect(url_for('login'))

@app.route('/streamer', methods=['GET', 'POST'])
def streamer() :
    if (request.method == 'POST') : #TODO add some form validation
        if (stream.is_running()) :
            stream.stop_streamer()
        else :
            stream.set_hashtag(request.form['hashtag'])
            stream.start_streamer()

    if (stream.is_running()) :
        running = True
        disabled = "disabled"
        button = 'stop'
        hashtag = stream.get_hashtag()
    else :
        running = False
        disabled=""
        button = 'start'
        hashtag = stream.get_hashtag()

    return render_template('streamer.html', disabled=disabled, button=button, hashtag=hashtag, running=running)

@app.route('/login', methods=['GET', 'POST'])
def login() :
    if (request.method == 'POST') :
        if (request.form['password'] == 'csisbest') :
            session['logged_in'] = True;
            session['username'] = request.form['username']
    if ('logged_in' in session and session['logged_in'] == True) :
        return render_template('test.html')
    else :
        return render_template('login.html')

@app.route('/logout') 
def logout() :
    if ('logged_in' in session) :
        session.clear()
        session['logged_in'] = False

    return redirect(url_for('login'))

if __name__ == '__main__' :
    app.run();
