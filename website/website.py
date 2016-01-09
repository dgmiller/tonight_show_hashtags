from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing
import sqlite3

import sys
import os
import traceback

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'..' ))
from tonight import streamer
from tonight import dataset
from tonight import fileutil
from tonight import sorter

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

@app.route('/sorter', methods=['GET', 'POST']) 
def sort_tweets() :
    datasets = os.listdir(dataset.RAW_DIR)
    tweet_text = ''

    if (request.method== 'POST') :
        dat = sorter.sorter(request.form['dataset'])

    return render_template('sorter.html', datasets=datasets)


@app.route('/import', methods=['GET', 'POST'])
def import_script() :

    if (request.method == 'POST') :
        f = request.files['script']

        if (request.form['overwrite'] == '0') :

            if (os.path.exists(os.path.join(dataset.SCRIPT_DIR, f.filename))) :
                flash("a script with that name already exists! select overwrite if you would like to overwrite it")

        elif (request.form['overwrite'] == '1') :
            f.save(os.path.join(dataset.SCRIPT_DIR, f.filename))
            dataset.delete_specific_cache(f.filename[0:-3])
            dataset.dataset.update_generators()
            

    return render_template('import.html')

@app.route('/viewer', methods=['GET', 'POST'])  #TODO this is tightly coupled with the current setup of dataset
def data_viewer() :
    filters = list(dataset.dataset.view_generators.keys())
    metas = list(dataset.dataset.data_generators.keys())
    datasets = os.listdir(dataset.RAW_DIR)
    text = ''

    if (request.method == 'POST') :
        dat = dataset.dataset(request.form['dataset'])

        try :
            for v in request.form.getlist('filter') : 
                dat = dat.intersect_view(v)

            result = dat.get_info(request.form['metas'])
            text = format_result(result) 
        except :
            text = "Hmm there was an error in the script\n"
            text += "Here is the stacktrace: \n\n"
            text += traceback.format_exc()

    return render_template('viewer.html', filters=filters, metas = metas, datasets = datasets, text = text)

def format_result(raw) :

    if (type(raw) == type(()) or type(raw) == type([])) :
        result = ''
        for l in raw :
            result += l.strip() + '\n\n'

        return result

    else :
        return raw

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
