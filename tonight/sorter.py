#! /usr/bin/env python

##this will be a sorter that will load some tweets and facilitate manual sorting

import os
import sys
import fileutil
import shutil
import dataset

ratings = ['1', '2', '3', '4', '5']

SORT_DIR = os.path.join(datset.DATA_DIR, 'sorted')

fileutil.create_folders([SORT_DIR])

#def create_sorted_filter(name) :

    #def inner(dset) :

        #lines = fileutil.read_file(os.path.join(SORT_DIR, 



class sorter (object) :

    def __init__(self, dataset_name) :
        self.dataset_name = dataset_name
        self.dset = dataset(dataset_name)
        #TODO here we will hardwire in some filters that we want to apply not sure how good of a design it is, but it should work
        self.folder = os.path.join(SORT_DIR, dataset_name)
        fileutil.create_folders([self.folder])
        self.current = self.get_next()

    def _translate_index(self, index) :
        ids = self.dset.get_info('id')
        return ids[index]
    
    def get_current_tweet(self) :
        return self.dset.get_info['tweet'][self.current]


    def get_size(self) :
        return len(self.dset.get_info('tweet'))


    ##assigns the current tweet to whichever rating is passed in
    # returns true if successful false if otherwise
    def rate_current_tweet(self, option) :

        if not (option in ratings) :
            return False;

        fileutil.append_file(os.path.join(self.folder, option), [str(self._translate_index(self.current))])
        self.current = self.get_next()
        return True;

    def get_next(self) :

        if (os.path.exists(os.path.join(self.folder, 'index'))) :
            lines, callback = fileutil.read_file(os.path.join(self.folder, 'index'))
            current = int(lines[-1].strip())
            callback([str(current + 1)])
            return current

        else :
            #create file, put in first entry and call again
            fileutil.write_file(os.path.join(self.folder, 'index'), ['0'])
            return get_next()


def main() :

    data = process.load_data(sys.argv[1])

    out = {}
    for r in ratings :
        out[r] = open(os.path.join(sorted_dir, r), 'a')

    for d in data :
        print('\n rate from 1 to 5, (1 being very unfunny, 5 being very funny)')
        print(process.string_tweet(d))

        response = input("?: ")

        while(response not in out) :
            print("invalid input, try again") 
            response = input("?: ")

        out[response].write(process.make_writeable(d))
        out[response].flush() #TODO this is just for debugging, should need when done


