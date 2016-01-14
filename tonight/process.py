#! /usr/bin/env python

#TODO eliminate bad words
#TODO convert winner tweets into correct format for processing
#TODO create nonexistant files
#TODO switch to a library for working with the xls files

import os;
import sys;
import re;
import nltk
import tempfile
import subprocess


TWEET_INDEX = 5; # the index of the actual tweet text in the CSV files

TAGGER_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "ark-tweet", "ark-tweet-nlp-0.3.2")
TAG_COMMAND = "./runTagger.sh --output-format conll --no-confidence {}"

DATA_DIR = "data"

RAW_DIR = os.path.join(DATA_DIR, "raw")

PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

SEP = "__"

############################################stuff for importing the winning tweets from the xls file

##\return a list split along the given separator ignoring things within quotes
#separator is defaulted to ,
def split_ignore_quotes(line, sep = ',') :
    result = []
    buffer = ''
    splitting = True;
    
    for c in line :

        if (c == '"') :
            splitting = not splitting
            
        elif (splitting) :
            if (c == sep) :
                result.append(buffer)
                buffer = ''
            else :
                buffer += c

        else : 
            buffer += c #TODO should I have to repeat this

    result.append(buffer)

    return result

## \return a list of strings with the text for the tweets
def parse_raw_data(dat_directory = "data") :
    result = [];

    for fname in os.listdir(dat_directory) :

        if re.match(r'.*\.csv.*', fname.lower()) : #check to see if they are csv files
            f = open(os.path.join(dat_directory, fname))
            raw = f.readlines();

            raw = [split_ignore_quotes(x) for x in raw[1:]]  #ignore the first line!
            result += [re.sub(r'""', '"', x[TWEET_INDEX]) for x in raw] #get the tweet and get rid of the extra "

    return result

################################################custom nltk stuff

##\param a list of tweets as single strings
#\return a list of lists of single words tokenized
def tokenize_tweets(data) :

    pattern = r'''(?x)
    ([A-Z]\.)+|
    \w+([-\'_]?[\w_]+)*|
    \.\s?\.\s?\.|
    \#\w+|
    \(at\)\w+|
    [$]\d+(\.\d+)?|
    \d+\%|
    \d+|
    [][.,;"'?():-_`~+!{}\\/|><]'''

    return [nltk.regexp_tokenize(x, pattern) for x in data]

##\param a list of lines, each line a separate tweet
#\return organized into the internal format which is
# [ [ (word, metadata1, . . . ), (word2, . . . ), . . . ], . . . ]
# where each sub list is a seperate tweet
def internal_format(raw_data, split_regex=SEP) :
    print("tokenizeing")
    #result = tokenize_tweets(raw_data)
    result = [x.strip() for x in raw_data]
    result = [x.split(' ') for x in result]
    print("splitting")
    final =[]
    for r in result :
        final.append([tuple(x.split(split_regex)) for x in r])

    return final 

##\return a list of lists of tuples of word/tag, it looks like this [ [ (word, part_of_speech), ... ], ... ]
def tag_tweets(tokenized_data) :

    return [nltk.pos_tag(x) for x in tokenized_data]  

############################################utility functions

def string_tweet (tweet) :
    buf = ''
    for t in tweet :
        buf += t[0] + ' '

    return buf

def print_tweets(tweets) :
    for t in tweets :
        print(string_tweet(t))


##\param the filename of a dataset found in the processed directory 
#\returns the data contained in the dataset in our standard format
def load_data(dataname) :
    f = open(os.path.join(PROCESSED_DIR, dataname))
    result = internal_format(f.readlines())
    f.close()
    return result

##\param takes a list of tweets in our format
#\returns a list of strings of our tweets in a writable format
def make_writeable(tweet) :
    joined = [SEP.join(x) for x in tweet]

    result = ' '.join(joined) + '\n'

    return result

################################################processor

def write_tweets(tweets, name) :
    f = open(os.path.join(PROCESSED_DIR,name), 'w')

    for t in tweets :
        f.write(make_writeable(t))

    f.close();

##reads in the content of of all files in the raw files directory
#\return a list of lists each list contains the lines of a file, with the first entry just being the name of the file
def read_in_raw_data() :
    result = []
    for f in os.listdir(path=RAW_DIR) :
        raw_file = open(os.path.join(RAW_DIR,f))
        result += [f] +  raw_file.readlines()
        raw_file.close()

    return result

##\param a list of lines to be tagged, it will be written to a file, so newlines should be included
#\return a list of lists of according to the internal format specified by internal_format(raw_data)
def tag_raw_data(raw) :
    (name, temp) = tempfile.mkstemp()
    (rname, rtemp) = tempfile.mkstemp()
    f = os.fdopen(name, 'w') #weird function because we are using a tempfile
    f.writelines(raw[1:])
    f.close()

    print("tagging")
    print(TAG_COMMAND.format(temp))
    f = os.fdopen(rname)
    result = subprocess.run(TAG_COMMAND.format(temp),stdout=f, cwd=TAGGER_PATH, shell=True) 
    print("finished tagging") 
    f.seek(0)
    result = f.readlines()
    f.close()
    result = [x.strip() for x in result]


    final_result = []
    buf = ''
    for i in range(len(result)) :
        if (result[i] == '') :
            final_result.append(buf[:-1]) #you have to cut of that extra ' '
            buf = ''
        else :
            pieces = result[i].split('\t')
            buf += pieces[0] + SEP + pieces[1] + ' '

    if (buf != '') :
        final_result.append(buf)


    final_result = internal_format(final_result)  #TODO find way to make it ignore all but the last _

    write_tweets(final_result, raw[0])

