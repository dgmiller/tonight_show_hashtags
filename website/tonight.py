from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
import sqlite3

DATABASE = '/tmp/test.db'
DEBUG = True
SECRET_KEY = 'whocares'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask("awesomeness")
app.config.from_object('tonight')

@app.route('/scraper', methods=['GET'])
def scraper() :
    if (request.method == 'GET' and 'test' in request.args) :
        print(request.args['test'])
    message = None
    return render_template('scraper.html')

@app.route('/') 
def main_page():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login() :
    if (request.method == 'POST') :
        if (request.form['password'] == 'csisbest') :
            session['logged_in'] = True;
    if ('logged_in' in session and session['logged_in'] == True) :
        return render_template('test.html')
    else :
        return render_template('login.html')

@app.route('/logout') 
def logout() :
    if ('logged_in' in session) :
        session['logged_in'] = False

    return redirect(url_for('login'))

if __name__ == '__main__' :
    app.run();
