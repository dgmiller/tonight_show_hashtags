#! /usr/bin/env python

import re
from selenium import webdriver
import time
import datetime

time_pattern = "%m/%d/%Y %H:%M"

min_offset = 46830 - (4 * 60) # the 4 * 60 thing is because I appear to be about 4 minutes off
max_offset = 46823 - (4 * 60) #this are the offsets for the timestamps from UTC, 

offset_scale = 10 #topsy offsets there search results in indexes of ten

##
#class for automatically finding and downloading tweets
class tweet_finder :

    ##\param tag the hashtag WITHOUT the #
    #\param startime the date for the left bound of the search
    #\param endtime the date for the end time of the search
    # the dates must be passed in as a string formated "MM/DD/YYYY HH:MM"
    # so far it has been accurate down to the minute of the tweet so that is good
    def __init__(self, tag, starttime=-1, endtime=-1) :
        self.driver = webdriver.PhantomJS() #set up web driver
        self.driver.implicitly_wait(10) #needs to wait for tweets to load
        self.tag = tag

        if (starttime != -1) :
            starttime = datetime.datetime.strptime(starttime, time_pattern)
            starttime = time.mktime(starttime.utctimetuple()) + min_offset
            
        if (endtime != -1) :
            endtime = datetime.datetime.strptime(endtime, time_pattern)
            endtime = time.mktime(endtime.utctimetuple()) + max_offset


        self.mintime = int(starttime)
        self.maxtime = int(endtime)
        self.offset = 0

    def __del__(self) :
        self.driver.quit() #close out internal web browser

    ##
    #will return a list of raw tweet strings, it includes other junk
    #if there are no more results will return an empty string
    #at the moment the middle line is the actual tweet itself
    def get_batch(self) :
        address = self.get_next_address()

        self.driver.get(address)

        result = self.driver.find_elements_by_class_name('result-tweet')

        self.offset += 1

        return [r.text for r in result]

    ##this formats the next address, it is really only used internally
    def get_next_address(self) :
        base = ['http://topsy.com/s?q=%23', "&sort=-date&type=tweet", "&mintime=", "&maxtime=", "&offset="] 

        address = base[0] + self.tag + base[1]

        if (self.offset > 0) :
            address += base[4] + str(self.offset * offset_scale)

        if (self.mintime != -1) :
            address += base[2] + str(self.mintime)

        if (self.maxtime != -1) :
            address += base[3] + str(self.maxtime)

        return address


def main() :
    t = tweet_finder('mydumbinjury', starttime="10/08/2015 00:00", endtime="10/19/2015 00:00")
    print(t.get_batch())
    print(t.get_batch())
    print(t.get_batch())

main()
