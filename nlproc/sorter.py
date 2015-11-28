#! /usr/bin/env python

##this will be a sorter that will load some tweets and facilitate manual sorting

import process
import os
import sys

ratings = ['1', '2', '3', '4', '5']

sorted_dir = os.path.join(process.DATA_DIR, 'sorted')


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


main()
