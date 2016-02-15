
import builtins

def meta(dset) :

    pos = dset.get_info('pos')


    result = []
    for p in pos :
        result.append(len(list(builtins.filter(lambda x: x != ',', p))))

    return result

#TODO yeah that was a pretty big oversight I guess, I should probably fix the whole filter thing shouldn't I?

def filter(dset) :
    count = dset.get_info('word_count')

    if count[0] <= 10 : #TODO I really need a way to eliminate this list of one thing, it is just so confusing ...
        return False
    
    else :
        return True
