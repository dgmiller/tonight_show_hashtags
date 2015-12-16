#! /usr/bin/env python

import re
from selenium import webdriver
import time
import datetime
from . import dataset
from . import fileutil
import os

#TODO clean up log from ghostdriver
#TODO see if there is a way to find the time of the tweet, it would make life much simpler

#TODO fix documentation, we are a little messy right now thanks to having to use time instead of offsets
time_pattern = "%m/%d/%Y %H:%M:%S"

min_offset = 46830 - (4 * 60) # the 4 * 60 thing is because I appear to be about 4 minutes off
max_offset = 46823 - (4 * 60) #this are the offsets for the timestamps from UTC, it appears to change from time to time so that limits our accuracy a fair bit

offset_scale = 10 

max_offset = 990 #topsy shows this many pages of results for one search

##
#class for automatically finding and downloading tweets
class tweet_finder :

    ##\param tag the hashtag WITHOUT the #
    #\param startime the date for the left bound of the search
    #\param endtime the date for the end time of the search
    #\param the delta for time in minutes, when the tweets are more concentrated it should be smaller (we want less than 100 tweets to occur in that delta, if there are more they will not be gathered, this is due to the way topsy is set up
    # the dates must be passed in as a string formated "MM/DD/YYYY HH:MM"
    def __init__(self, tag, starttime, endtime, last_delta=0) :
        self.driver = webdriver.PhantomJS() #set up web driver
        self.driver.implicitly_wait(10) #needs to wait for tweets to load 
        self.tag = tag

        starttime = datetime.datetime.strptime(starttime, time_pattern) #convert from a string to a time
        starttime = time.mktime(starttime.utctimetuple()) + min_offset
            
        endtime = datetime.datetime.strptime(endtime, time_pattern)
        endtime = time.mktime(endtime.utctimetuple()) + max_offset


        self.mintime = int(starttime)
        self.maxtime = int(endtime)
        self.currentmin = int(self.mintime) + last_delta
        self.currentmax = self.maxtime
        self.offset = 0 
        self.exhausted = False

        self.focus_initialized = False #TODO this seems clunky . . .

    def __del__(self) :
        self.driver.quit() #close out internal web browser

    ##this will set the time frame to ensure that we are getting as much as we can without having any results
    #truncated
    #not thread safe (though really not any of this is thread safe)
    #returns True if it changed to another meaningful offset, false if it has exhausted the tweets
    def focus(self) :
        self.offset = max_offset

        if (self.exhausted) :
            return False

        if (self.focus_initialized) : 
            #TODO, when we are over a certain threshold, just continually check to the maximum, otherwise it takes forever
            delta = (self.currentmax - self.currentmin) * 2 #the * 2 is just to offset the constant division we will otherwise be doing
            if (delta == 0) : #TODO make this work better here
                delta = 100
            self.currentmin = self.currentmax
            self.currentmax += delta
        else :
            self.focus_initialized = True

        if (self.currentmax >= self.maxtime) :
            self.currentmax = self.maxtime
            self.exhasted = True


        focused = False 

        while (not focused) :
            address = self.get_next_address()
            print(address)
            self.driver.get(address)
            result = self.driver.find_element_by_id('module-results')

            print(result.text)

            if (re.match(r'.*no.*tweet.*found.*', result.text.lower())) :
                focused = True
            else :
                delta = int((self.currentmax - self.currentmin) / 2)
                self.currentmax -= delta
                self.exhasted = False

        self.offset = 0

        return True

    ##
    #will return a list of raw tweet strings, it includes other junk
    #if there are no more results will return an empty list
    #at the moment the middle line is the actual tweet itself
    def get_batch(self) :
        address = self.get_next_address()

        self.driver.get(address)

        result = self.driver.find_element_by_id('module-results')

        if (re.match(r'.*no.*tweet.*found.*', result.text.lower())) :
            return []

        result = result.find_elements_by_class_name('result-tweet')
        print(len(result))
        self.offset += offset_scale
        
        return [r.text for r in result]

    ##this formats the next address, it is really only used internally
    def get_next_address(self) :
        base = ['http://topsy.com/s?q=%23', "&sort=-date&type=tweet", "&mintime=", "&maxtime=", "&offset="] 

        address = base[0] + self.tag + base[1]

        address += base[2] + str(self.currentmin)

        address += base[3] + str(self.currentmax)
        
        if (self.offset > 0) :
            address += base[4] + str(self.offset)

        return address

    ## this method returns the raw text of the tweet itself
    @staticmethod
    def parse_tweet(tweet) :
        return tweet.split('\n')[1]


##Singleton class for controlling the web scraper
class scraper_driver :

    QUEUE_FILE = os.path.join(dataset.DATA_DIR, "scraper_queue")
    QUEUE_FILE_SEP = ";"

    ##puts an order to download a dataset on the list of things to be downloaded
    def add_to_queue(self, tag, start, end) :
        order = tag + scraper_driver.QUEUE_FILE_SEP + start + scraper_driver.QUEUE_FILE_SEP + end 
        fileutil.append_file(scraper_driver.QUEUE_FILE, (order,))

    ##returns a copy of the queue as a tuple of tuples
    # in the format ( (hashtag, starttime, endtime), . . . )
    def get_queue (self) :
        result = fileutil.read_file(scraper_driver.QUEUE_FILE)
        result = [tuple(r.split(scraper_driver.QUEUE_FILE_SEP)) for r in result]
        return tuple(result)


    ##deletes the top element from the list
    def _delete_top(self) :
        lines = fileutil.read_file(scraper_driver.QUEUE_FILE)
        fileutil.write_file(scraper_driver.QUEUE_FILE, lines[1:]) #TODO this is not threadsafe!! we need to slap the mutex on these two lines or else things will probably go wrong someday

    def download_next(self) :
        target = self.get_queue()[0]

        t_finder = tweet_finder(target[0], target[1], target[2])
        bucket = dataset.dataset.make_new(target[0])
        bucket_dataset = bucket[0]
        append_tweets = bucket[1]
    
        while(t_finder.focus()) :
            batch = t_finder.get_batch()
            count = 1
            while (batch != []) :
                print(str(count) + ' batch(es) complete')
                tweets = [tweet_finder.parse_tweet(b) for b in batch] 
                append_tweets(tweets)
                count += 1
                batch = t_finder.get_batch()
            print("focusing")

        self._delete_top()

        return bucket_dataset


driver = scraper_driver()
#there! singelton by convention, only ever call this method!
def get_driver() :
    return driver

def main() :
    #for now we can just change the options right here
    tag = 'AirportFail'
    start = "07/29/2015 00:00:00"
    end = "07/31/2015 00:00:00"
    
    t_finder = tweet_finder(tag, start, end)

    start = str.replace(start, '/', '_')
    start = str.replace(start, ' ', '_')
    end = str.replace(end, '/', '_')
    end = str.replace(end, ' ', '_')
    filename = tag + '-' + start + '-' + end

    out = open(filename, 'w+') #open the file for updating if it already exists


    while(t_finder.focus()) :
        batch = t_finder.get_batch()
        count = 1
        while (batch != []) :
            print(str(count) + ' batch(es) complete')
            tweets = [tweet_finder.parse_tweet(b) for b in batch] 
            out.writelines([t + '\n' for t in tweets])
            count += 1
            batch = t_finder.get_batch()
        print("focusing")

