##This script returns the top 100 words used in the entire dataset and their frequency
# it also serves as an example for a script that creates a summary to view, known as a display
# the are in the lower half of the second column on the viewer page of the website


# the website will look for a function called display, and will pass it a dataset object
def display(dset) :

    dset = dset.intersect_view('RT') #The get_view function returns a new dataset object with the 
                                       # specified filter applied to it, you can use any filter that is on the website
                                       # including one you may have added 
                                       # 
                                       # Here I am using the intersect view, this just returns the intersection of the current view
                                       # with the filter that you want applied. This way if they choose other views on the website they will also be applied
                                       # to our results. Without this it would just show the same results every time
                                       #
                                       # all future get_info and get_view calls on the returned dataset will only take into
                                       # account the tweets selected by the filter
                                       # also it is not shown here, but you can stack filters and it works like intersecting the current filter with the new one

    words = dset.get_info('get_tokens') # the get_tokens script is already on the website, and we can catch its output in here like this

    if dset.get_current_size() <= 0 : # check to make sure not everything is eliminated by the filter, and there are tweets to work with
        return "there are no tweets in this dataset!"

    word_set = {}

    for l in words : # when we asked for get_tokens it sent back a list of lists of single words strings
        for w in l : # we are going to smoosh them into one dict counting as we go
            if w in word_set :
                word_set[w] += 1

            else :
                word_set[w] = 1


    word_set = list(word_set.items()) # switch to a list of two item tuples

    word_set = sorted(word_set, key = lambda x : x[1], reverse=True) # sort them, (if you are unfamiliar with lambda, feel free to ask about it)

    if dset.name in word_set[0][0] : # chances are the most common word will be the hashtag, which we will want to ignore . . .
        word_set = word_set[1:]

    if len(word_set) > 100 : #make sure the list is big enough before slicing it
        word_set = word_set[:100]

    result = ''  # We want to return a single string to be seen by the person viewing it
                 # All display functions should return a single string, formatted however you would like
    for word, frequency in word_set :

        result += '\t' + word + ' : ' + str(frequency) + '\n'

    return result
