##This script returns the top 100 words used in the entire dataset
# it also serves as an example for a script that creates a summary to view, known as a display


# the website will look for a function called display, and will pass it a dataset object
def display(dset) :

    dset = dset.get_view('RT') #The get_view function returns a new dataset object with the 
                               # specified filter applied to it, you can use any filter that is on the website
                               # including one you may have added 
                               # all future get_info and get_view calls on the returned dataset will only take into
                               # account the tweets selected by the filter

    words = dset.get_info('tokenize') # the tokenize script is already on the website, and we can catch its output in here like this

    if len(words) <= 0 : # check to make sure not everything is eliminated by the filter
        return "there are no tweets in this dataset!"

    word_set = {}

    for l in words : # when we asked for tokenize it sent back a list of lists of single words strings
        for w in l : # we are going to smoosh them into one dict counting as we go
            if w in word_set :
                word_set[w] += 1

            else :
                word_set[w] = 1


    word_set = list(word_set.items()) # switch to a list of two item tuples

    word_set = sorted(word_set, key = lambda x : x[1], reverse=True) # sort them, (if you are unfamiliar with lambda, feel free to ask about it)

    if dset.name in word_set[0][0] : # chances are the most common word will be the hashtag, which we will want to ignore . . .
        word_set = word_set[1:]

    if len(word_set) > 100 : #make sure the list is big enough
        word_set = word_set[:100]

    result = ''  # We want to return a single string to be seen by the person viewing it
    for word, frequency in word_set :

        result += '\t' + word + ' : ' + str(frequency) + '\n'

    return result
