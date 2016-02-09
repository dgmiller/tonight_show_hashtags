



def meta(dset) :

    words = dset.get_info("get_tokens")


    result = []

    for tweet in words :
        result.append([])

        for i in range (len(tweet) - 1) :

            trigram = ' '.join([tweet[i], tweet[i+1]])
            result[-1].append(trigram)


    return result


def display(dset) :

    trigrams = dset.get_info("bi_grams")

    tri_set = {}

    for t in trigrams :
        for w in t : # we are going to smoosh them into one dict counting as we go
            if w in tri_set :
                tri_set[w] += 1

            else :
                tri_set[w] = 1


    tri_set = list(tri_set.items()) # switch to a list of two item tuples

    tri_set = sorted(tri_set, key = lambda x : x[1], reverse=True) # sort them, (if you are unfamiliar with lambda, feel free to ask about it)

    if len(tri_set) > 100 : #make sure the list is big enough before slicing it
        tri_set = tri_set[:100]

    result = ''  # We want to return a single string to be seen by the person viewing it
                 # All display functions should return a single string, formatted however you would like
    for gram, frequency in tri_set :

        result += '\t' + gram + ' : ' + str(frequency) + '\n'

    return result


