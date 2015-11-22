#! /usr/bin/env python
##tools to detect patterns in the pos of these tweets

import process
import os


##\param the filename of a dataset found in the processed directory (specified by process.py)
#\returns the data contained in the dataset in our standard format
def load_data(dataname) :
    f = open(os.path.join(process.PROCESSED_DIR, dataname))
    result = process.internal_format(f.readlines())
    f.close()
    return result


##\param a single tweet in the standard format 
#\return a string of the POS tags in the order the appear in the tweet
def extract_tags(tweet) :
    result = ''

    for t in tweet :
        result += t[1]

    return result[:-1] #for some reason it leaves a \n on there


##\param a list of tweets in the standard format
#also start and stop are the lower and upper lengths for a pattern
#\return a dict of pos-patterns found and there frequencies
def find_patterns(tweets, start = 3, stop = 6) :
    result = {}

    for tweet in tweets : 
        tweet = extract_tags(tweet)

        for l in range(start, stop + 1) : #for every length between start and stop

            for i in range(len(tweet)) : #start at the beginning of each character in the tweet

                if (i + l < len(tweet) -1) :
                    key = tweet[i : i + l] 

                    if key in result :
                        result[key] += 1 #increment the pattern if it exists, or else make it
                    else :
                        result[key] = 1

    return result

##\param tweets, list of tweets in standard format
#\return the number of tweets that that pattern occurs in
def pattern_count(tweets, pattern) :
    count = 0;

    for tweet in tweets : 
        tweet = extract_tags(tweet)
        if (pattern in tweet) :
            count += 1

    return count


##\param data a dictionary like the kind returned form find_pattern
#\param length how many results to show
#\returns a sorted list of tuples of frequency,pattern pairs
#[ (frequency, pattern) . . . ]
def get_top(data, length) : #TODO the method I chose is easy to code, but is somewhat inefficient
    data = data.items()
    result = []

    for d in data :
        result.append((d[1], d[0]))

    result.sort(key=lambda x : x[0], reverse=True) #wahoo! I hardly ever get to use lambda!

    return result[:length]
