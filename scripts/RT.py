##A filter that will filter out any retweets, also used as an example for how to make a filter

import re #you can import the standard libraries as well as numpy, let Kolten know if you want a different library


##The website will look for function named filter in the file uploaded
# this function recieves a dataset object, which is normally the representation of all the tweets under one hashtag
# with filters it will contain a single tweet as opposed to all of them
def filter(dset) :
    #the dataset object has two methods that you care about, this is one of them

    tweet_text = dset.get_info('tweet')

    # the get_info method will return a list of all the data stored under a certain label
    # the list is in the same order every time, and the positions correspond to each other
    # when you ask for two different labels
    # you can use any label you see on the website in the upper second columns 
    # even the ones you made yourself
    # in the case of filters the list returned will always only have one element in it << This is important

    tweet_text = tweet_text[0] #this is necessary, as get_info returns a list
                               # but because this is a single tweet it is always a list of size one

    if (re.match(r'^RT.*$',tweet_text) ) : #simple regex to see if it is a retweet
        return False  #False means we do not want to view this tweet
    else : 
        return True   #True means we do want to view this tweet

# this function will be called once for each tweet in the full dataset to decide whether to include it or not
