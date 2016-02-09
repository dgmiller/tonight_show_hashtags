##A script that tokenizes the words in the tweets, also an example of how to make a 
# metadata generator

#This example is more complicated than the rest, you may want to read the RT.py and top_100.py first
# you can also skip down to the meta function if you just want to see how to make a metagenerator, this first stuff is not as important for that
import os
import sys
import re
import tempfile
import subprocess



#These lines are used to access an external tagger, they do not have anyting to do with metadata generation in general
TAGGER_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "nlproc", "ark-tweet", "ark-tweet-nlp-0.3.2") #TODO this is tightly coupled, we need a way to obtain the path << ignore this, just a note to myself
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

#as a side note, you can include other functions besides the one the website looks for in these files, please do! more functions = better code almost always


# Okay the website is looking for a function called meta, meta for metadata
# You are given a dataset object as normal
def meta(dset) :  #IMPORTANT, you should not use filters when generating metadata, it will mess things up, the metadata generation should be applied to every tweet in datset
    
    raw = dset.get_info('tweet') #Take the text of the tweets

    result = tag_raw_data(raw) #run it through the tagger, this is returning a list of words, breaking up the long tweet text into seperate words

    final_result = []

    for r in result :
        final_result.append([])
        for t in r :
            final_result[-1].append(t[0]) #We are creating a list of lists. Each tweet gets its own list of words 

    return final_result # as a return value, you should send back a list, each element in the list should correspond to one tweet, and should be the data for the tweet that is normally in that position
                        # what the list contains is up to you, in this case it is a list of lists! (which is confusing I know) but it could be strings, or it could be numbers or whatever really
                        # it can not be python objects unfortunately, but any of the basic data types and containers will be fine

