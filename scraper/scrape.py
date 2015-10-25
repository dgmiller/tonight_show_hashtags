#! /usr/bin/env python

import re
from selenium import webdriver
import time
import datetime

#TODO clean up log from ghostdriver
#TODO see if there is a way to find the time of the tweet, it would make life much simpler

#TODO fix documentation, we are a little messy right now thanks to having to use time instead of offsets
time_pattern = "%m/%d/%Y %H:%M:%S"

min_offset = 46830 - (4 * 60) # the 4 * 60 thing is because I appear to be about 4 minutes off
max_offset = 46823 - (4 * 60) #this are the offsets for the timestamps from UTC, 

offset_scale = 10 #topsy offsets there search results in indexes of ten

##
#class for automatically finding and downloading tweets
class tweet_finder :

    ##\param tag the hashtag WITHOUT the #
    #\param startime the date for the left bound of the search
    #\param endtime the date for the end time of the search
    #\param the delta for time in minutes, when the tweets are more concentrated it should be smaller (we want less than 100 tweets to occur in that delta, if there are more they will not be gathered, this is due to the way topsy is set up
    # the dates must be passed in as a string formated "MM/DD/YYYY HH:MM"
    def __init__(self, tag, starttime, endtime, delta=3) :
        self.driver = webdriver.PhantomJS() #set up web driver
        self.driver.implicitly_wait(2) #needs to wait for tweets to load TODO increase later
        self.tag = tag

        self.tdelta = delta * 60

        starttime = datetime.datetime.strptime(starttime, time_pattern)
        starttime = time.mktime(starttime.utctimetuple()) + min_offset
            
        endtime = datetime.datetime.strptime(endtime, time_pattern)
        endtime = time.mktime(endtime.utctimetuple()) + max_offset


        self.mintime = int(starttime)
        self.maxtime = int(endtime)
        self.currenttime = int(self.mintime)
        self.offset = 0 #TODO do I really need this?

    def __del__(self) :
        self.driver.quit() #close out internal web browser

    ##
    #will return a list of raw tweet strings, it includes other junk
    #if there are no more results will return an empty list
    #at the moment the middle line is the actual tweet itself
    def get_batch(self) :
        address = self.get_next_address()

        if (address == '') :
            return []

        self.driver.get(address)

        #TODO search for false results to more quickly verify that it is not working

        result = self.driver.find_elements_by_class_name('result-tweet')

        if (len(result) > 0) :
            return [r.text for r in result]
        else :
            return self.get_batch() #yay recursion!

    ##this formats the next address, it is really only used internally
    def get_next_address(self) :
        base = ['http://topsy.com/s?q=%23', "&sort=-date&type=tweet&perpage=100", "&mintime=", "&maxtime=", "&offset="] 

        address = base[0] + self.tag + base[1]

        self.currenttime += self.tdelta

        if (self.currenttime >= self.maxtime) :
            return ''

        address += base[2] + str(self.mintime)

        address += base[3] + str(self.currenttime)

        return address

def parse_tweet(tweet) :
    return tweet.split('\n')[1]

def main() :
    #for now we can just change the options right here
    tag = 'mydumbinjury'
    start = "07/14/2015 0:00:00"
    end = "07/16/2015 0:00:00"
    
    t_finder = tweet_finder(tag, start, end, delta=10)

    start = str.replace(start, '/', '_')
    start = str.replace(start, ' ', '_')
    end = str.replace(end, '/', '_')
    end = str.replace(end, ' ', '_')
    filename = tag + '-' + start + '-' + end

    out = open(filename, 'w')


    batch = t_finder.get_batch()
    count = 0
    while (batch != []) :
        tweets = [parse_tweet(b) for b in batch] 
        out.writelines([t + '\n' for t in tweets])
        count += 1
        print(str(count) + ' batch(es) complete')
        batch = t_finder.get_batch()

main()
