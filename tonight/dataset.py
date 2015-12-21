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

    data_generators = {"reflect" : lambda x : x.get_info("tweet"), "chop" : lambda x : tuple(range(len(x.get_info("tweet")) // 2))}

    #----static initializtion stuff ---------------------------------------------
    fileutil.create_folders([RAW_DIR, META_DIR]) #not sure how good of an idea this is, but it should work


    #----static methods---------------------------------------

    ##this method will return the name passed in to it, or else
    #it will return a unique name that is close
    @staticmethod
    def get_unique_name(name) : #TODO I should probably throw a mutex on this to make it threadsafe

        used_names = os.listdir(RAW_DIR)

        if name in used_names :

            count = 2
            while ((name + str(count)) in used_names) :
                count += 1

            name += str(count)

        open(os.path.join(RAW_DIR, name), 'x').close() #create the file immediately
        return name

    ##creates a new dataset
    # will ensure that the name is unique, and based on the hashtag
    # \returns a tuple, the first item is a reference to the object that was made
    #           the second is a method, it takes a list of strings and will append them to the raw data
    #           it is only to be used before calling any other methods, that behavior is not enforced at the moment
    @staticmethod
    def make_new(hashtag) :
        result = dataset()
        result.hashtag= hashtag
        if hashtag[0] == '#' :  #get rid of # in hashtag if it is there
            result.hashtag = hashtag[1:]

        result.name = dataset.get_unique_name(hashtag)

        return (result, result.get_injection_method())

    ##this function returns a method that can be used to inject text into the raw dataset
    # the fuction returned takes a list or tuple of lines to write, do not let it fool you
    def get_injection_method(self) :
        def inject_raw_data(lines) :
            fileutil.append_file(os.path.join(RAW_DIR, self.name), lines)

        return inject_raw_data


    ##this will load an already existing dataset
    @staticmethod
    def load(name) :
        result = dataset()
        result.name = name

        try :
            raw_data = fileutil.read_file(os.path.join(RAW_DIR, result.name)) 

        except FileNotFoundError :
            return None

#        i = 0
        #running = ['', 0]
#        while (running[1] < 5) : #quick and dirty algorithm to detect hashtag
        #    #TODO come up with a better solution, this one requires the dataset to be fairly large to work, and is fairly ineffecient anyway
            #tag = re.match(r'^.*(#\S+).*$', raw_data[i]).group(1)

            #if (tag == running[0]) :
                #running[1] += 1
            #else :
                #running[0] = tag
                #running[1] = 0

        #dataset.hashtag = running[0][1:]

        result.hashtag = name
        return result

#----non static methods --------------------------------------------------------------------------------------------------------
    def __init__(self) :
        self.data = []
        self.viewset = set()

    ##this function makes a copy for the purpose of returning a view
    # it is a shallow copy really
    def _copy_self(self) :
        copy = dataset()

        if not self.data : #make sure that the data has been generated before making the copy
            self._populate_dataset()

        copy.data = self.data
        copy.name = self.name
        copy.hashtag = self.hashtag 

        return copy

    def get_current_view(self) : #TODO this is feeling a little messy
        for index in self.viewset :
            yield self.data[index]


    def get_view(self, key) :
        new_view = self._copy_self()

        new_view.viewset = self._get_viewset(key)

        return new_view

    def _get_viewset(self, key) :
        path = os.path.join(META_DIR, self.name, key)

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

        return tuple([x[key] for x in self.get_current_view()])

    def _populate_dataset(self) :
        lines = fileutil.read_file(os.path.join(RAW_DIR, self.name))

        for l in lines :
            self.data.append({})
            l = l.split(DATA_SEP)

            self.data[-1]["user"] = l[0]
            self.data[-1]["time"] = l[1]
            self.data[-1]["tweet"] = l[2]

        self.viewset = tuple(range(len(self.data))) #TODO, this is in the wrong place

