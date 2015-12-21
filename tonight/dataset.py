import sys
import os
from . import fileutil
import re

DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'data')
RAW_DIR = os.path.join(DATA_DIR, 'raw')
VIEW_DIR = os.path.join(DATA_DIR, 'view')
META_DIR = os.path.join(DATA_DIR, 'meta')
DATA_SEP = "___"

class dataset :
    #TODO clean up static vs nonstatic and add comments
    #TODO seperate metadata generators from view generators
    #TODO better way of keeping track of real index with views, in case one wants to create dependent views
    #TODO way to tell if raw data exists or not? may not be necessary . . .


#----static initializtion stuff ---------------------------------------------
    fileutil.create_folders([RAW_DIR, META_DIR, VIEW_DIR]) #not sure how good of an idea this is, but it should work
    data_generators = {"reflect" : lambda x : x.get_info("tweet"), "chop" : lambda x : tuple(range(len(x.get_info("tweet")) // 2))}
    
#----non static methods --------------------------------------------------------------------------------------------------------
    def __init__(self, hashtag) :
        self.name = hashtag 
        if (self.name[0] == "#") : #get rid of preceding # if it is there 
            self.name = self.name[1:]

        self.hashtag = hashtag

        self.data = []
        self.viewset = set() #TODO initialize data now? or wait? if now we need to check if the file exists or not

    ##this function returns a method that can be used to inject text into the raw dataset
    # the fuction returned takes a list or tuple of lines to write, do not let it fool you
    def get_injection_method(self) :
        def inject_raw_data(lines) :
            fileutil.append_file(os.path.join(RAW_DIR, self.name), lines)

        return inject_raw_data

    ##this function makes a copy for the purpose of returning a view
    # it is a shallow copy really
    def _copy_self(self) :
        copy = dataset(self.hashtag)

        if not self.data : #make sure that the data has been generated before making the copy
            self._populate_dataset()

        copy.data = self.data #we will share state on these items 
        copy.name = self.name #TODO is name and hashtag really necessary?
        copy.hashtag = self.hashtag 

        return copy

    def _get_current_view(self) : 
        for index in self.viewset :
            yield self.data[index]


    def get_view(self, key) :
        new_view = self._copy_self()
        new_view.viewset = self._generate_viewset(key)

        return new_view

    def _generate_viewset(self, key) :
        path = os.path.join(VIEW_DIR, self.name, key)

        if not (os.path.exists(path)) : #if no cached version exists then make one
            result = dataset.data_generators[key](self) #TODO deal with different data types #TODO, eliminate slight repetition of code here
            fileutil.create_folders(os.path.dirname(path)) #make sure folder exists
            fileutil.write_file(path, [str(x) for x in result])

        lines = fileutil.read_file(path)

        return set([int(x.strip()) for x in lines])

    def _generate_data(self, key) :
        path = os.path.join(META_DIR, self.name, key)

        if not (os.path.exists(path)) : #if no cached version exists then make one
            result = dataset.data_generators[key](self) #TODO deal with different data types
            fileutil.create_folders(os.path.dirname(path)) #make sure folder exists
            fileutil.write_file(path, result)

        lines = fileutil.read_file(path)

        for l, d in zip(lines, self.data) : #TODO make so that it will sense if it is out of date and renew cache
            d[key] = l #TODO add some number and list converting here

    def get_info(self, key) : 
        if not (self.data) :
            self._populate_dataset()

        if not (key in self.data[-1]) :
            self._generate_data(key)

        return tuple([x[key] for x in self._get_current_view()])

    def _populate_dataset(self) :
        lines = fileutil.read_file(os.path.join(RAW_DIR, self.name))

        for l in lines :
            self.data.append({})
            l = l.split(DATA_SEP)

            self.data[-1]["user"] = l[0]
            self.data[-1]["time"] = l[1]
            self.data[-1]["tweet"] = l[2]

        self.viewset = tuple(range(len(self.data))) 

