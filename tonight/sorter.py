#! /usr/bin/env python

##this will be a sorter that will load some tweets and facilitate manual sorting

import os
import sys
from . import fileutil
import shutil
from . import dataset

ratings = ['1', '2', '3', '4', '5']

SORT_DIR = os.path.join(dataset.DATA_DIR, 'sorted')
SIGNAL = '*'
OLD_BUFFER = 10

fileutil.create_folders([SORT_DIR])

def create_sorted_filter(name) :

    def inner(dset) :

        try :
            lines = fileutil.read_file(os.path.join(SORT_DIR,dset.name,name))
            lines = [int(l) for l in lines]

            if dset.get_info('id')[0] in lines :

                return True
            else :
                return False

        except :
            return False


    return inner

def add_sorted_filters() :
    for r in ratings :
        dataset.add_additional_filter(r, create_sorted_filter(r))


add_sorted_filters()

class sorter (object) :

    def __init__(self, dataset_name, line=-1) :
        self.dataset_name = dataset_name
        self.dset = dataset.dataset(dataset_name).get_view('RT')
        self.dset = self.dset.intersect_view('clean')
        #TODO here we will hardwire in some filters that we want to apply not sure how good of a design it is, but it should work
        self.folder = os.path.join(SORT_DIR, dataset_name)
        fileutil.create_folders([self.folder])
        if (line == -1) :
            self.current = self._get_initial()
        else :
            self.current = line

    def _translate_index(self, index) :
        ids = self.dset.get_info('id')
        return ids[index]
    
    def get_current_tweet(self) :
        if (self.current == -1) :
            return "and that was the last one! no more tweets here"
        return self.dset.get_info('tweet')[self.current]


    def get_size(self) :
        return len(self.dset.get_info('tweet'))


    ##assigns the current tweet to whichever rating is passed in
    # returns true if successful false if otherwise
    # it could be false if the line was already rated while you took forever to do it as well
    def rate_current_tweet(self, option) :

        if not (option in ratings or self.current == -1) :
            return False;

        result = False


        lines, callback = fileutil.read_write(os.path.join(self.folder, 'index'))

        if SIGNAL in lines[self.current] :
            fileutil.append_file(os.path.join(self.folder, option), [str(self._translate_index(self.current))])
            lines[self.current] = str(self.current)

        #self.current = _get_current(lines) #TODO make it smoother and clearer that this is a one off object and once rated once is useless without further modification
        callback(lines)

        return result

    def _get_initial(self) :

        if (os.path.exists(os.path.join(self.folder, 'index'))) :
            lines, callback = fileutil.read_write(os.path.join(self.folder, 'index'))

            current = self._get_current(lines)
            callback(lines)
            return current

        else :
            #create file, put in first entry and call again
            fileutil.write_file(os.path.join(self.folder, 'index'), ['0*'])
            return 0

    #potentially modifies list passed into it
    def _get_current(self, lines) :
        result = -1

        if (len(lines) > OLD_BUFFER) :
            for l in lines[:-OLD_BUFFER] :

                if (SIGNAL in l) :
                    result = int(l[:-1])
                    break

        if (result == -1) :
            result = lines[-1]

            if SIGNAL in result :
                result = result[:-1]

            result = int(result) + 1
            if (result < self.get_size() and result > 0) :
                lines.append(str(result) + SIGNAL) 

            else :
                result = -1

        return result

