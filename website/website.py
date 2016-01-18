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


@app.route('/sorter')
def sort_tweets_redirect() :
    return redirect(url_for('sort_tweets', tweet_id=-1, tweet_text=" ", dset=False))

@app.route('/sorter/<tweet_id>/<path:tweet_text>/<dset>', methods=['GET', 'POST']) 
def sort_tweets(tweet_id, tweet_text, dset) :
    datasets = os.listdir(dataset.RAW_DIR)

    if (request.method== 'POST') :
        if 'submit' in request.form :
            dat = sorter.sorter(request.form['dataset'], line = int(tweet_id))
            dataset.delete_specific_cache(request.form['submit']) #TODO come up with more efficient way to do this, right now it will delete all such data
            dat.rate_current_tweet(request.form['submit'])

        dat = sorter.sorter(request.form['dataset'])
        tweet_text = dat.get_current_tweet()

        return redirect(url_for('sort_tweets', dset=request.form['dataset'], tweet_id=dat.current, tweet_text=tweet_text))
    
    return render_template('sorter.html', datasets=datasets, dset=dset, tweet_text=tweet_text)


@app.route('/import', methods=['GET', 'POST'])
def import_script() :

    if (request.method == 'POST') :
        f = request.files['script']

        if (request.form['overwrite'] == '0') :

            if (os.path.exists(os.path.join(dataset.SCRIPT_DIR, f.filename))) :
                flash("a script with that name already exists! select overwrite if you would like to overwrite it")
                return render_template('import.html')

        f.save(os.path.join(dataset.SCRIPT_DIR, f.filename))
        dataset.delete_specific_cache(f.filename[0:-3])
        dataset.dataset.update_generators()
        

    return render_template('import.html')

@app.route('/viewer', methods=['GET', 'POST'])  #TODO this is tightly coupled with the current setup of dataset
def data_viewer() :
    filters = list(dataset.dataset.view_generators.keys())
    metas = list(dataset.dataset.data_generators.keys())
    displays = list(dataset.dataset.display_generators.keys())
    datasets = os.listdir(dataset.RAW_DIR)
    text = ''
    selected_dataset = ''
    selected_filters = []
    selected_meta = ''

    if (request.method == 'POST') :
        dat = dataset.dataset(request.form['dataset'])

        try :
            for v in request.form.getlist('filter') : 
                dat = dat.intersect_view(v)

            if (request.form['metas'] in displays) :
                text = dat.get_display(request.form['metas'])
            else :
                result = dat.get_info(request.form['metas'])
                text = format_result(result) 

        except :
            text = "Hmm there was an error in the script\n"
            text += "Here is the stacktrace: \n\n"
            text += traceback.format_exc()

        selected_dataset = request.form['dataset']
        selected_filters = request.form.getlist('filter')
        selected_meta = request.form['metas']

    return render_template('viewer.html', filters=sorted(filters), metas = sorted(metas), displays=sorted(displays), datasets = sorted(datasets), text = text, sdataset = selected_dataset, sfilters = selected_filters, smeta = selected_meta)

def format_result(raw) :

    if (type(raw) == type(()) or type(raw) == type([])) :
        result = ''
        for l in raw :
            result += str(l).strip() + '\n\n'

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
        if (request.form['password'] == 'fallon') :
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
