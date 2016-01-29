#! /usr/bin/env python
##tools to detect patterns in the pos of these tweets

import os

##\param a list of tweets in the standard format
#also start and stop are the lower and upper lengths for a pattern
#\return a dict of pos-patterns found and their frequencies
def find_patterns(tags, start = 3, stop = 6, tag_filter=default_filter) :
    result = {}

    for tweet in tags : 

        if (tag_filter) :
            tweet = [tag_filter(t) for t in tweet]   #replace values
            tweet = ''.join([t for t in tweet if t])  #join back into a string, discarding None



        for l in range(start, stop + 1) : #for every length between start and stop

            for i in range(len(tweet)) : #start at the beginning of each character in the tweet

                if (i + l < len(tweet) -1) :
                    key = tweet[i : i + l] 

                    if key in result :
                        result[key] += 1 #increment the pattern if it exists, or else make it
                    else :
                        result[key] = 1

    return result


##a simple filter for use in the tag_filter parameter of find_patterns
# \param a single tag
#\return a single tag, or else None if the tag is not to be used
# see the ark-twitter tagger's docs for the tags used by it
def simple_filter(tag) :

    if (tag in 'NO^SZ') :
        return 'N'
    elif (tag in 'VLMY') :
        return 'V'
    else :
        return None

def default_filter(tag) :
    return tag


##\param tweets, list of tweets in standard format
#\return the number of tweets that that pattern occurs in
def pattern_count(tweets, pattern, tag_filter=default_filter) :
    count = 0;

    for tweet in tweets : 
        tweet = extract_tags(tweet)

        if (tag_filter) :
            tweet = [tag_filter(t) for t in tweet]   #replace values
            tweet = ''.join([t for t in tweet if t])  #join back into a string, discarding None

        if (pattern in tweet) :
            count += 1

    return count


##\param data a dictionary like the kind returned form find_pattern
#\param length how many results to show
#\returns a sorted list of tuples of frequency,pattern pairs
#[ (frequency, pattern) . . . ]
def get_top(data, length) : #TODO the method I chose is easy to code, but is somewhat inefficient so far it has been fast enough 
    data = data.items()
    result = []

    for d in data :
        result.append((d[1], d[0]))

    result.sort(key=lambda x : x[0], reverse=True) #wahoo! I hardly ever get to use lambda!

    return result[:length]


def display(dset) :

    tags = dset.get_info('pos')
    results = get_top(find_patterns(tags), 100)


    final = ''
    for r in results :
        final += r[1] + ' : ' + str(r[0]) + '\n'


    return final
