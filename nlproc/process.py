#! /usr/bin/env python
#in python 3! I will probably have to switch to 2 eventually but I learned how to use the NLTK in 3

#TODO make a better tokenizer for tweets
#TODO eliminate punctuation and hashtags

import os;
import re;
import nltk;


TWEET_INDEX = 5; # the index of the actual tweet text in the CSV files

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

##\param a list of tweets as single strings
#\return a list of lists of single words tokenized
def tokenize_tweets(data) :

    pattern = r'''(?x)
    ([A-Z]\.)+|
    \w+([-\']?\w+)*|
    \.\s?\.\s?\.|
    \#\w+|
    \(at\)\w+|
    [$]\d+(\.\d+)?|
    \d+\%|
    \d+|
    [][.,;"'?():-_`~+!{}\\/|><]'''

    return [nltk.regexp_tokenize(x, pattern) for x in data]
    
