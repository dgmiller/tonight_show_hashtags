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
max_offset = 46823 - (4 * 60) #this are the offsets for the timestamps from UTC, it appears to change from time to time so that limits our accuracy a fair bit

offset_scale = 10 #topsy offsets their search results in indexes of ten TODO I may not need this anymore . . . 

max_len = 100 #topsy only returns the top 100 results of any search, so we have to make our searches less than that
to_few_perc = 0.20 #if we get 20% of the max len then are search is to narrow and we should widen it

##
#class for automatically finding and downloading tweets
class tweet_finder :

    ##\param tag the hashtag WITHOUT the #
    #\param startime the date for the left bound of the search
    #\param endtime the date for the end time of the search
    #\param the delta for time in minutes, when the tweets are more concentrated it should be smaller (we want less than 100 tweets to occur in that delta, if there are more they will not be gathered, this is due to the way topsy is set up
    # the dates must be passed in as a string formated "MM/DD/YYYY HH:MM"
    def __init__(self, tag, starttime, endtime, init_delta=60, last_delta=0) :
        self.driver = webdriver.PhantomJS() #set up web driver
        self.driver.implicitly_wait(10) #needs to wait for tweets to load 
        self.tag = tag

        self.tdelta = init_delta * 60

        starttime = datetime.datetime.strptime(starttime, time_pattern) #convert from a string to a time
        starttime = time.mktime(starttime.utctimetuple()) + min_offset
            
        endtime = datetime.datetime.strptime(endtime, time_pattern)
        endtime = time.mktime(endtime.utctimetuple()) + max_offset


        self.mintime = int(starttime)
        self.maxtime = int(endtime)
        self.currenttime = int(self.mintime) + last_delta
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

        result = self.driver.find_element_by_id('module-results')

        if (result.text == "No tweets found.") : #TODO this is a mess, I need to come back an clean in up, but lets just see if it works first
            print('none')
            self.increase_delta()
            return self.get_batch()

        result = result.find_elements_by_class_name('result-tweet')
        print(len(result))
        
        if (len(result) >= max_len) :
            self.decrease_delta()
        elif (len(result) > 0) :

            if (len(result) < int(to_few_perc * max_len)) :
                self.increase_delta()

            return [r.text for r in result]

        return self.get_batch() #yay recursion!

    ##this formats the next address, it is really only used internally
    def get_next_address(self) :
        base = ['http://topsy.com/s?q=%23', "&sort=-date&type=tweet&perpage=100", "&mintime=", "&maxtime=", "&offset="] 

        address = base[0] + self.tag + base[1]

        temp_max = self.currenttime + self.tdelta

        print(self.tdelta * 60)

        if (self.currenttime == self.maxtime) : # at the moment it will skip the last chunk, so give a good buffer to the time interval you want to retrieve
            return ''

        if (temp_max > self.maxtime) :
            temp_max = self.maxtime


        address += base[2] + str(self.currenttime)

        address += base[3] + str(temp_max)

        self.currenttime = temp_max

        return address

    def increase_delta(self) :
        self.tdelta *= 2

    def decrease_delta(self) :
        self.currenttime -= self.tdelta #roll back changes to be safe
        self.tdelta /= 2

def parse_tweet(tweet) :
    return tweet.split('\n')[1]

def main() :
    #for now we can just change the options right here
    tag = 'mydumbinjury'
    start = "07/14/2015 01:00:00"
    end = "07/16/2015 00:00:00"
    
    t_finder = tweet_finder(tag, start, end)

    start = str.replace(start, '/', '_')
    start = str.replace(start, ' ', '_')
    end = str.replace(end, '/', '_')
    end = str.replace(end, ' ', '_')
    filename = tag + '-' + start + '-' + end

    out = open(filename, 'w+') #open the file for updating if it already exists


    batch = t_finder.get_batch()
    count = 0
    while (batch != []) :
        tweets = [parse_tweet(b) for b in batch] 
        out.writelines([t + '\n' for t in tweets])
        count += 1
        print(str(count) + ' batch(es) complete')
        batch = t_finder.get_batch()

main()
