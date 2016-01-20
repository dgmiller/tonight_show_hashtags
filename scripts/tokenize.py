#! /usr/bin/env python

import os;
import sys;
import re;
import tempfile
import subprocess


TAGGER_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "nlproc", "ark-tweet", "ark-tweet-nlp-0.3.2") #TODO this is tightly coupled, we need a way to obtain the path
TAG_COMMAND = "./runTagger.sh --output-format conll --no-confidence {}"

##\param a list of lines to be tagged, it will be written to a file, newlines will be added
#\return a list of tuples of tuples, of the format [ ( (word, pos_tag), (word, pos_tag) . . . )  . . . ]
# each outer tuple is one tweet, and each inner tuple is one word in that tweet
def tag_raw_data(raw) :
    (name, temp) = tempfile.mkstemp()
    (rname, rtemp) = tempfile.mkstemp()
    f = os.fdopen(name, 'w') #weird function because we are using a tempfile
    f.writelines([r + '\n' for r in raw])
    f.close()

    #call external tagger
    print(TAG_COMMAND.format(temp))
    f = os.fdopen(rname)
    result = subprocess.call(TAG_COMMAND.format(temp),stdout=f, cwd=TAGGER_PATH, shell=True) 
    #read them back in
    f.seek(0)
    result = f.readlines()
    f.close()
    result = [x.strip() for x in result]


    final_result = []
    buf = []
    for i in range(len(result)) :
        if (result[i] == '') :
            final_result.append(tuple(buf)) #you have to cut of that extra ' '
            buf = []
        else :
            pieces = result[i].split('\t')
            buf.append( (pieces[0],pieces[1] ) )

    if (buf != []) :
        final_result.append(buf)

    
    return final_result



def meta(dset) :

    raw = dset.get_info('tweet')

    result = tag_raw_data(raw)

    final_result = []

    for r in result :
        final_result.append([])
        for t in r :
            final_result[-1].append(t[0])

    return final_result

