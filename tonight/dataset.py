import sys
import os
from . import fileutil
import re

DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'data')
RAW_DIR = os.path.join(DATA_DIR, 'raw')
FILTER_DIR = os.path.join(DATA_DIR, 'filter')



class dataset :

    #----static initializtion stuff ---------------------------------------------
    fileutil.create_folders([RAW_DIR, FILTER_DIR]) #not sure how good of an idea this is, but it should work


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

        def inject_raw_data(lines) :
            fileutil.append_file(os.path.join(RAW_DIR, result.name), lines)

        return (result, inject_raw_data)


    ##this will load an already existing dataset
    @staticmethod
    def load(name) :
        self.name = name

        raw_data = fileutil.read_file(os.path.join(RAW_DIR, self.name)) 

        i = 0
        running = ['', 0]
        while (running[1] < 5) : #quick and dirty algorithm to detect hashtag
            #TODO come up with a better solution, this one requires the dataset to be fairly large to work, and is fairly ineffecient anyway
            tag = re.match(r'^.*(#\S+).*$', raw_data[i]).group(1)

            if (tag == running[0]) :
                running[1] += 1
            else :
                running[0] = tag
                running[1] = 0

        self.hashtag = running[0][1:]
