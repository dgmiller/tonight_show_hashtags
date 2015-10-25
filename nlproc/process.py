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
    

##\return a list of lists of tuples of word/tag, it looks like this [ [ (word, part_of_speech), ... ], ... ]
def tag_tweets(tokenized_data) :

    return [nltk.pos_tag(x) for x in tokenized_data]  


##\return a count of the number of items in a list that match both content and position
#must be of equal length
#it is adapted to work with tags from the nltk tagger, so only send it lists of tags
def match_count(list1, list2) :
    count = 0
    for i in range(len(list1)) :
        if (list1[i][0:2] == list2[i][0:2]) :
            count += 1

    return count
    
##
#this method returns a tuple of two equalized lists 
#the shorter one will have null characters to offset the larger one (by default)
#if already equal, will return the two strings unchanged
#\return at tuple (longer_string, equalized_shorter_string)
def equalize(list1, list2, fill = '\0') :

    if (len(list2) == len(list1)) :
        return (list1, list2)

    elif (len(list2) > len(list1)) :
        shorter = list1;
        longer = list2;
        
    else :
        shorter = list2;
        longer = list1;

    delta = len(longer) - len(shorter)

    shorter += fill * delta #fill in the extra space

    return (longer, shorter)

##this method will cause a list to wrap around in place by the given offset
#for example:
#
#offset("offset", 3)
#returns "setoff"
def offset(list1, offset_by) :
    return list1[offset_by :len(list1)] + list1[0:offset_by] 


##\param a list of words (probably tags)
# \return the percentage their highest match as a float < 1
def shift_match(list1, list2) :

    working = equalize(list1, list2, fill = ["NULL"])

    highest = 0;

    for i in range(len(list1)) :   
        current = match_count(list1, offset(list2, i)) #this will check the match at every possible sequential permutation of the two lists

        if (current > highest) : #if it is equal we will stick with the first match
            highest = current

    return highest / float(len(list1))


##
#this will attempt to group the tweets according to any found pattern
#
def group_tweets(tagged_data) :
    THRESHOLD = 0.2
    result = []
    caught = False

    for tweet in tagged_data :

        if (len(tweet) == 0) :
            continue #TODO filter input before it gets here

        match_count = 0;

        for i in range(len(result)) :
            rtags = [x[1] for x in result[i][0]]
            ttags = [x[1] for x in tweet] #this just extracts the tags ignoring the words
            
            if (shift_match(rtags, ttags) >= THRESHOLD) :
                result[i].append(tweet)
                caught = True
                break
        
        if (not caught) :
            result.append([tweet])

        else :
            caught = False

    #DEBUG
    buf = ''
    for r in result :
        buf += str(len(r)) + ' '
    
    print(buf)

    return result


def print_tweet(tagged) :
    for t in tagged :
        buf = ''
        for w in t :
            buf += w[0] + ' ' 
        print(buf)
